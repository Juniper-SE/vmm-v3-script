# How to use Juniper VMM

release 0.91
## Overview
This script is used to create configuration files, which will be used to create and run VMs (Virtual Machines) on Juniper's VMM infastructure.
The scripts has been modified to work with VMM 3.0 

## Caveat

The latest version for paramiko (version 4.0.0), support for DSSKey has been deprecated. 

The problem is ncclient 0.6.15 which is required for ansible for junos,  still use DSSKey when it uses the paramiko modules. 
so you need to upgrade ncclient to version 0.7.0, but during the upgrade, you may encounter the following message

       Installing collected packages: ncclient
         Attempting uninstall: ncclient
           Found existing installation: ncclient 0.6.15
           Uninstalling ncclient-0.6.15:
              Successfully uninstalled ncclient-0.6.15
       ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
       junos-eznc 2.7.4 requires ncclient==0.6.15, but you have ncclient 0.7.0 which is incompatible.
       Successfully installed ncclient-0.7.0


## update on the script
new features has been added into the scripts :

- vpn is no longer required, everything is handled by zscaler connect
- jump host is no longer required
- using jinja2 template to create configuration for junos devices. Currently it support configuration for the following :
    * address family : inet, inet6, , iso, mpls
    * protocols : isis, mpls, rsvp, ldp, pcep, bgp-ls, srv6
- topology of point-to-point connection between junos devices can be generated automatically, for both bridge assignment and address (ipv4/ipv6) allocation
- On VMM 3.0, configuration of PC's VM is no longer written to the disk image when the VM was started for the first time, so on this script, the configuration of the PC is pushed using ssh, therefore PC VMs must be assigned with IP address
- the IP address assignment to the PC VMs is done using dhcp with node GW as the dhcp server
- create wireguard configuration for direct connection into the nodes in the Lab. 


## The supported VMs :
- vJunos Switch
- vJunos Router
- vJunos Evolved
- vMX
- vSRX
- Apstra fabric controller
- PC with ubuntu OS 
- PC with centos OS
- bridge using Alpine linux to provide Delay or packet loss between Nodes

## Requirement
This script requires the following :
- Python3 (this script requires Python3)
- passlib library 
- paramiko library 
- yaml library


## VM images
Before the script is used, the VM images must be available on the VMM.

Please upload the VM images into directory /vmm/data/user_disks/<your_user_name>

If you are connecting to VMM Lab @ Quincy, then you can copy my images from /vmm/data/user_disks/irzan/images/.

If you are using different VMM lab, then you have to copy the file into it.

## Scripts

This tool consist of the following script
- [vmm.py](../vmm.py)
- [lib1.py](../lib1.py)
- [param1.py](../param1.py)
- lab configuration (lab.yaml)
- [requirements.txt](../requirements.txt)

## lib1.py
This script is the library with functions declaration used by the main scripts (`vmm.py`)

## param1.py
This script provide the parameters required by the library

## lab.yaml
This YAML file provide the definition of the lab topology

please edit this file for the following :
- the VMM pod which will be used
- the jump host to access the VMM lab
- JNPR Lab Domain password (to access vmm server)
  - if you don't want to hardcode your VMM password into file lab.yaml, your can set environment variable VMMPASSWORD with your JNPRLAB domain password

        export VMMPASSWORD="what ever is your password"

- the disk images for the VMs
- fabric topology for point-to-point connection between VMs
- the VM, its type, its OS, management IP address and network interfaces (and its bridge) for connection to other devices.

Please refer to the sample configuration under directory [Lab](Lab/)

## requirements.txt

This file contains list of python3 libraries required by the script

on your workstation, install it using the following command

        pip3 install -r requirements.txt


## vmm.py
This script is the user interface, which will read the configuration `lab.yaml` and call the library from `lib1.py1

There are different arguments required by this script
- argument `upload` : to create VMM configuration files and upload them into VMM pod
- argument `start` : to start the topology inside the VMM
- argument `stop` : to stop the topology inside the VMM 
- argument `list` :  to get the list of running VMs
- argument `set_gw`: to send configuration of gateway (ip address on other interface (em1,em2, etc) and DHCP server configuration)
- argument `set_host`: to send configuration to Linux VMs
- argument `create_gw_config`: to create wireguard configuration


## Caution

- when the script is used to start the topology, any existing running topology will be stopped and unbound. Please backup the existing topology if needed.
- on one pod location, only one VMM topology can run. If you need to run multiple topology, then you need to run those topology on different VMM pod.

## Accessing the VMM Lab

VMM lab can only be accessed using Juniper's Laptop because it is located on Juniper's Intranet and required zscaler to access it.

To check on which VMM server that you have active topology, can be found at [https://vmm.englab.juniper.net](https://vmm.englab.juniper.net)

Information about the availability of VMM servers (online status and available capacity) can be found at [https://vmm.englab.juniper.net/default_live](https://vmm.englab.juniper.net/default_live)

## Prepare python3 virtual environment

Screenshot recording for this can be found [here](https://asciinema.org/a/738124)

1. Create python3 virtual environment to the script. 

       python3 -m venv ~/python3/vmmlab
       
2. activate the python3 virtual environment

       source ~/python3/vmmlab/bin/activate

3. Clone the [script's repository](https://github.com/Juniper-SE/vmm-v3-script) 

       cd ~/git
       git clone git@github.com:Juniper-SE/vmm-v3-script.git

        or 

       cd ~/git
       git clone https://github.com/Juniper-SE/vmm-v3-script.git

4. Install the necessary python3 package into the virtual environment

       cd vmm-v3-script
       pip3 install -r requirements.txt

5. Install ansible for junos

       ansible-galaxy collection install juniper.device

## VMM topology configuration file

1. Create configuration file for the lab **lab.yaml** or use one of the lab.yaml available inside directory Lab.

       cd ~/git/vmm-v3-script/Lab
       mkdir topoNew
       cd topoNew
       vi lab.yaml

       or

       cd ~/git/vmm-v3-script/Lab/
       cd topo1


2. In this document, we are going to take a look into the configuration for lab [**topo1**](../Lab/topo1/lab.yaml)

       cd ~/git/vmm-v3-script/Lab
       cd topo1
       vi lab.yaml

3. This part of the configuration, define the name of the lab, and it will use as directory name to store configuration of this topology on the vmm server

       ---
       name: topo1

4. This part of the configuration, define the vmm pod where we want to run the topology, the home directory on the vmm server, and the username to access the vmmserver. You can harcode the password to access the vmm server on file lab.yaml, with field **vmmpassword** or you can set environment variable VMMPASSWORD before you run the script.

       pod: 
         type: vmm
         vmmserver: q-pod27-vmm.englab.juniper.net
         user: irzan
         #vmmpassword: AnaMabokCoy
         home_dir : /vmm/data/user_disks/irzan

5. For the vmm server, select the vmm pod that has enough token required for your topology (check the token availability at this url [https://vmm.englab.juniper.net/default_live](https://vmm.englab.juniper.net/default_live)). Remember to put the FQDN of the vmm server, which is the name of the pod and suffix **-vmm.englab.juniper.net** 

6. This part of the configuration define the login information that we want to configure on vJunosVM

       junos_login:
         login: admin
         password: pass01

7. This part of the configuration define the disk image for the VM/vJunosVM. the disk image must be available on the vmm server home directory

       images:
         gw: images/gw.qcow2
         ubuntu: images/ubuntu24.04.qcow2
         bridge: images/bridge.qcow2
         vjunos_router: images/vJunos-router-25.2R1.9.qcow2
         vjunos_evolved: images/vJunosEvolved-25.2R1.8-EVO.qcow2
         <os_name>: <disk_images>


        gw: images/gw.qcow2, "gw:" or <os_name> refer to the field "os" on each nodes, and "images/gw.qcow2" or <disk_images> is the disk image file on the home directory for the vmm server

        
7. This part of the configuration define connectivity between nodes/vJunosVM in the topology

       fabric:
         subnet: 10.100.0.0/24
         topology:
         - [ 0x17, r1, ge-0/0/1, r2, ge-0/0/1 ]
         - [ 0x17, r1, ge-0/0/2, r4, et-0/0/1 ]
         - [ 0x17, r2, ge-0/0/2, r3, et-0/0/1 ]
         - [ 0x17, r4, et-0/0/2, r3, et-0/0/2 ]

       subnet: define the ipv4 subnet which will be used for point-to-point ip address between nodes/JunosVM
       subnet6: define the ipv6 subnet which will be used for point-to-point ip address between nodes/JunosVM. If subnet6 is not defined, then script will assume to use ipv6 local address

       topology: define how the nodes/vJunosVM are connected to each other, it will have multiple lines, where each line define point-to-point connection between two nodes/vJunosVM. 

       for example "[ 0x17, r1, ge-0/0/1, r2, ge-0/0/1 ]", define connection between node "r1" and "r2", where port "ge-0/0/1" of "r1" is connected to port "ge-0/0/1" of "r2", and the first field, in this case "0x17", define what will be configured on that point-to-point link. 

       the value of the first field is an integer, which can be in hexadecimal or decimal or binary, and the value of each bit of this field are the following 

        value for the field status:
        bit 0 : ipv4 --> family ipv4 is enabled, and ipv4 address will be allocated from subnet
        bit 1 : ipv6 --> family ipv6 is enabled, and ipv6 address will be allocated from subnet6 or local ipv6 address
        bit 2 : iso --> family iso is enabled
        bit 3 : mpls --> family mpls and protocol mpls are enabled
        bit 4 : isis --> protocol isis is enabled
        bit 5 : rsvp --> protocol rsvp is enabled
        bit 6 : ldp --> protocol ldp is enabled

8. This part of the configuration define the nodes inside the topology

       vm:
         gw:
           type: gw
           interfaces:
             em0: 
               bridge: external
             em1: 
               bridge: mgmt
               family:
               inet: 172.16.11.254/24
               dhcp_range: 172.16.11.1-172.16.11.200
          r1:
            type: vjunos_router
            interfaces:
              mgmt: 
                bridge: mgmt
                family:
                  inet: 172.16.11.1/24
                  gateway4: 172.16.11.254
              lo0:
                family:
                  inet: 10.100.255.1/32
                  iso: 49.0001.0001.0001.0001.00
                  inet6: fc00:dead:beef:ffff::1/128
                protocol:
                  isis: passive
              ge-0/0/0:
                bridge: r1ge0
                mtu: 9000
          r2:
            type: vjunos_router
            interfaces:
              mgmt: 
                bridge: mgmt
                family:
                  inet: 172.16.11.2/24
                  gateway4: 172.16.11.254
              lo0:
                family:
                  inet: 10.100.255.2/32
                  iso: 49.0001.0001.0001.0002.00
                  inet6: fc00:dead:beef:ffff::1/128
                protocol:
                  isis: passive
              ge-0/0/0:
                bridge: r2ge0
                mtu: 9000
          client1:
            type: pchpv1
            interfaces:
            em0: 
               bridge: mgmt
               family:
                 inet: 172.16.11.10/24
                 gateway4: 172.16.11.254
               em1: 
                 bridge: r1ge0
               em2: 
                 bridge: r2ge0
               em3: 
                 bridge: r3et0
               em4: 
                 bridge: r4et0
        
       for example, on this topology, there are four nodes, gw, r1, r2, and client1

       node "gw" must be defined inside the topology, because this node will act as gateway/jumphost between juniper intranet and the other nodes inside the topology. This is the only node with connection to juniper intranet.  Port em0 is connected to juniper intranet, because it is connected to bridge "external", and it will get ip address automatically from juniper intranet dhcp server.

       node "gw" will have another interface, for example em1, where the management interface of other node (linux VM, vJunos) will be connected to and they has to be assigned with the bridge and assigned with ip address from the same subnet. on this interface, another field is define, dhcp_range (ip pool), which will be used by the script to generate configuration for the dhcp server.

       each node will have field "os" and "type".
        
       the field "type" supported by this script can be found inside file param1.py, for example type can be gw, vjunos_router, vjunos_switch, vjunos_evolved, pchpv1, pcmedium, etc.
       on file param1.py, each "type" define three parameters, number of vcpu (ncpus), amount of RAM (memory), and parameter required by vmm/qemu to run the nodes (setvar)


## Step by Step guide on how to use the script

Screenshot recording for this can be found [here](https://asciinema.org/a/737867)

1. Change directory to the lab topology that you want to deploy. For example, the following is when you want to deploy lab topo1

       cd ~/git/vmm-v3-script/Lab
       mkdir topo1
       cd topo1
       

2. Run the script with argument `upload`, to upload the configuration files into VMM server. The script will ctreate the configurations under directory `./tmp`. Files inside these directory will be uploaded into VMM server. You have to run this script, while you are inside the lab directory, for example if your lab name is topo1, then your lab directory will be ~/git/vmm-v3-script/Lab/topo1, and file lab.yaml must be on this directory.

       ls lab.yaml
       ../../vmm.py upload

3. Run the script with argument `start`, to start the topology on VMM. Remember any active topology will be stop and destroyed. Remember to backup the configuration of any existing running topology

       ../../vmm.py start

4. the script will modify file ~/.ssh/config, to include all the VM/vJunosVM define in lab.yam, so you can open ssh session directly into the nodes without the need to specify the jumphost (node gw) manually. If you look into file ~/.ssh/config, this modification are added after line **### by vmm-v3-script ###**

       less ~/.ssh/config


5. Verify that node GW is up and running, by initiating ssh session into it. The username to access node GW is **ubuntu** and poassword is **pass01**

       ssh gw

6. Run the script with argument `set_gw`, to configure other interfaces of node gw (interface em1, em2, etc), upload ssh key and dhcp server configuration. Node **GW** will be acting as DHCP server and tftp (for ZTP) for VM ubuntu/centos/vJunos VM in the topology

       ../../vmm.py set_gw

7. Verify that node GW has been configured.

       ssh gw
       sudo systemctl status kea-dhcp4-server
       ls -la /srv/tftp
       ip addr show
       exit

8. Run the script with argument `set_host`, to configure Linux VM, such has hostname, change interface configuration from dhcp to static, and upload ssh key.

       ../../vmm.py set_host

9. vJunos VM in the topology, such as vJunos-Router, vJunos-Switch, and vJunos-Evolved will be assigned with initial configuration using ZTP. the initial configuration for these vJunos VM are created by the script during **../../vmm.py upload**. It may take few minutes for the ZTP process to finish.


10. To verify that VMs in the topology are running, you can open ssh session into node **vmm** and access serial console of the VM/Nodes

       ssh vmm
       vmm list
       vmm serial -t r1
       vmm serial -t gw
       vmm serial -t pe1

11. Or you can open ssh session directly from your workstation  or from node **gw**

       ssh r1
       ssh r2

12. Now the lab is ready and can be used
