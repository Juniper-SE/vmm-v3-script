# Installing Vsphere (VCenter and ESXi) in Juniper VMM
This document provides information on how to install vsphere (vcenter and esxi) in the VMM environment.

## Topology
The logical topology of the testbed is as follows :
![topology](topology.png)

## Source Code
To generate topology and configuration of the lab in Juniper VMM, use the [script](../../../../../)

Lab configuration file required for the script can be found [here](../lab.yaml)

## Caveat

for unknown reason, ESXi node may lost its network connection, and the only way to resolve it, is by rebooting the node.

you can access the node through VNC and restart the node.

## Credential to access node/devices

node | username| password| type access
--|--|--|--
esxi1|root|Jun1peR|web access/management/console
esxi2|root|Jun1peR|web access/management/console
esxi3|root|Jun1peR|web access/management/console
vcsa|root|Jun1peR|ssh/console
gw|centos|pass01|ssh/serial console
gw|root|pass01|ssh/serial console

## Devices
The devices/nodes in the topology are :

1. GW
    - gateway between juniper's intranet and testbed network
    - this devices also provide the following function :
        - NTP server
        - DNS server
        - http server
        - dhcp server
        - Sock proxy server for http access from your workstation
        - gateway for VM's connection to external 
2. vsphere nodes 
    - vcsa : vcenter nodes
    - esxi1 : esxi compute node 1
    - esxi2 : esxi compute node 2
    - esxi3 : esxi compute node 3

subnet in the testbed

Network | Subnet | usage
--|--|--
mgmt | 172.16.10.0/24| for management and vmotion network
lan1 | 172.16.11.0/24| for storage (vsan)
lan2 | multiple subnets with vlan| for connection to VMs

## Disk images for vsphere
I have created customized disk images for vcenter (which is version 6.7) and it is available on on my home directory, /vmm/data/user_disks/irzan/vmware. 

You can copy the files and put them into your home directory.

for vcenter, there are two disk images, vcsa67.vmdk and vcsa67disk2.vmdk.

vcsa67.vmdk is the primary disk for vcenter, which is customized from vcenter ova. 

The original vcenter ova installation has 15 disk images. Disk1 is the primary disk, disk2 is the second disk with installation file required for vcenter initialization, and disk3 - disk15 are disk images used for various function, such as db storage, log, etc.

To run vcenter on VMM, I customize the disk image by doing the following 

    - extend the size of disk1 to accomodate disk3 - disk15
    - create new partition and logical volume on disk1 (add 10 partition/logical volume) and copy the content of disk3 - disk15 to these partitions/logical volumes
    - disk2 is still required for vcenter initialization.

ESXi disk images

    - for esxi disk images, each esxi node requires a unique disk image. if you try to use the same disk image for two different ESXi node, when you try to add these esxi into vcenter, it will fail.
    - I have created 3 disk images for esxi, esxi1.vmdk, esxi2.vmdk and esxi3.vmdk. if you need to have additional esxi nodes, then you can create your own image, and name is as esxi4.vmdk, esxi5.vmdk, etc, and upload it into vmm.


## VSAN or no VSAN
when running vsphere on vmm, there is an option to enable or disable vsan.

To enable vsan, on the lab configuration file , [lab.yaml](../lab.yaml), under **vm** > **vcsa**, set **vsan** option to **yes** or **True**

![vsan_enable](vsan_enable.png)

When VSAN is enabled, then lab initialization script will create additional two disk per esxi node.


## Setup the testbed
1. Edit [lab.yaml](../lab.yaml) according to your setup, such as username, jumphost, vmm pod, ssh key, etc.
2. Use this [script](../../../../../) to generate and upload configuration into VMM, and start the topology
3. Add the content of file tmp/ssh_config into your ~/.ssh/config, to allow easy access using ssh into nodes inside the VMM. the ssh configuration will allow you to do ssh without the need to specify the jumphost manually.
4. Wait until all nodes are up and running, test connectivity by ssh into node **gw**.
5. upload files [install_gw.sh](../gw/install_gw.sh) and [nginx.conf](../gw/nginx.conf) into node **gw**, and run script **install_gw.sh** on node **gw**. Wait until node **gw** reboot process is finish
![install_gw](install_gw.png)
6. Now NTP, dhcp, DNS and HTTP server function is running on node **gw**

## IP address configuration of vcenter
1. By default vcenter and esxi nodes are configured with dhcp
2. Change the ip addresses of vcenter and esxi with the following :
        nodes | IP address | gateway | DNS
        --|--|--|--
        vcsa| 172.16.10.200/24|172.16.10.1|172.16.10.1
        esxi1| 172.16.10.201/24|172.16.10.1|172.16.10.1
        esxi2| 172.16.10.202/24|172.16.10.1|172.16.10.1
        esxi3| 172.16.10.203/24|172.16.10.1|172.16.10.1

        node| login user| password
        -|-|-
        vcsa|root|Jun1p3R
        esxi1|root|Jun1p3R
        esxi2|root|Jun1p3R
        esxi3|root|Jun1p3R


3. Get the VNC port for node **vcsa**. use script [vmm.py](../../../vmm.py) to get vnc port information
4. Open ssh session to node **gw** with port forwarding to the vnc port from previous step.
![vnc_port](vnc_port.png)
5. open vnc client on your workstation, and open vnc session to the local port
![vncviewer](vncviewer.png)
6. Now you can change the ip address of node **vcsa** (ip address, netmask, default gateway, dns server, and hostname)
7. Repeat step 3 - 6 for node **esxi1**, **esxi2**, and **esxi3***
8. From node **gw**, verify that ip address of the vsphere nodes are reachable.
![ping](ping.png)

9. For unknown reason, esxi nodes may lost its network connect. One way to solve is by doing continuous ping from gw. Use this [script](../gw/check_esxi.sh) to do continuous ping from GW to vsphere nodes

![ping2](ping2.png)

## Setting the datastore on esxi nodes.
1. open ssh session to node **proxy** proxy and keep this session open when you are accessing the web interfaces of nodes on the VMM lab.
![proxy](proxy.png)
2. Use mozilla firefox, and set the proxy with the following configuration
- manual proxy configuration
- SOCKS hosts : 127.0.0.1
- Port : 1080
- Type : SOCKS v4
![proxy2](proxy2.png)
3. Datastore name
    Node | datastore name
    -|-
    esxi1 | datastore1
    esxi2 | datastore2
    esxi3 | datastore3

3. Open web session to esxi1 dashboard, https://172.16.10.201
4. login and change the datastore according to the above table
5. repeat step 3-4 on node esxi2 and esxi3

## initial configuration of vcenter
1. open web session to vcenter server appliance management interface, https://172.16.10.200:5480/
2. Click Setup to start initialization process, and enter user/password : root/Jun1p3R
3. On **appliance configuration**, set the **System Name** to the ip address of the VCSA : 172.16.10.200
![vcsa1](vcsa1.png)
4. Create the new SSO domain :
    - SSO domain name : vsphere.local
    - set SSO password : for example Jun1p3R-01

![vcsa2](vcsa2.png)

5. you can opt-out for CEIP

6. When you click **FINISH**, the initialization process will start. Wait until  it finishs

![vcsa3](vcsa3.png)
![vcsa4](vcsa4.png)

7. SSH into vcsa, go into shell, and edit file /etc/hosts, and add the following entry

        172.16.10.200 vcsa
        172.16.10.201 esxi1
        172.16.10.202 esxi2
        172.16.10.203 esxi3

![vcsa5](vcsa5.png)

8. On vcsa, verify that it can ping esxi1, esxi2 and esxi3
![vcsa6](vcsa6.png)

9. On mozilla firefox, open web session to VCenter client, https://172.16.10.200/ui

![vcenter1](vcenter1.png)

10. The vcenter is running with trial license.

![vcenter2](vcenter2.png)

11. Create datacenter : DC1
![vcenter3](vcenter3.png)

12. Create cluster : CL1. If vsan is enabled when you deploy the topology on the VMM, then vSPhere DRS and vSAN can be enabled, otherwise just leave it as it is.

![vcenter4](vcenter4.png)

13. Click Add hosts, and add esxi1, esxi2, and esxi3. Use username/password : root/Jun1p3R
![vcenter5](vcenter5.png)
![vcenter6](vcenter6.png)

14. Wait until esxi1, esxi2, and esxi3 added into vcenter
15. Click configure cluster, and create 3 distributed switch
    Distributed switch| used for | uplink
    -|-|-
    DSW1 | management and vmotion| vmnic0
    DSW2| vsan | vmnic1
    DSW3 | VM's network | vmnic2

![vcenter7](vcenter7.png)
![vcenter7a](vcenter7a.png)

16. Set static ip address for vmotion
    node | ip address| gw
    -|-|-
    esxi1| 172.16.10.204/24|172.16.10.1
    esxi2| 172.16.10.205/24|172.16.10.1
    esxi3| 172.16.10.205/24|172.16.10.1

![vcenter8](vcenter8.png)

17. Set static ip address for vsan
    node | ip address
    -|-
    esxi1| 172.16.11.201/24
    esxi2| 172.16.11.202/24
    esxi3| 172.16.11.203/24

![vcenter9](vcenter9.png)

18. If vsan is enabled, then claim disk. Set the drive type to flash, and on each esxi node, select disk2 as capacity tier and disk3 as cache tier.
![vcenter10](vcenter10.png)

19. Finish the cluster configuration, wait untuk cluster initialization is finish

20. vsphere is configured and you can start configuring the DPG (Distributed port group) and VM



