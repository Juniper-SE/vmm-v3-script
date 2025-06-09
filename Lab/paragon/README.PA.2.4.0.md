# How setup Paragon 2.4.1 Lab on VMM
## topology

![topology](images/topology_lab.jpg)

## note
Tested with paragon automation 2.4.1
based on this [documentation](https://www.juniper.net/documentation/us/en/software/juniper-paragon-automation2.4.0/installation-guide/index.html).

## Devices in the lab

- vJunosRouter : pe1, pe2, pe3, pe4, p1, p2, p3, p4, pe5
- cRDP : linux with containerd + juniper crpd as route reflector
- Linux client: client (to provide test traffic) (linux ubuntu)
- Bridge : br1, br2, br3( linux bridge between junos node to simulate link failure, delay and packet loss) (linux alpine)

- Kubernetes cluster for Paragon Automation
    - Node1, Node2, Node3, Node4 : Paragon 2.4.1 Virtual Appliance


## Credential to access devices
- Ubuntu linux
    - user: ubuntu
    - password: pass01
- Alpine linux/Bridge
    - user: alpine
    - password: pass01
- vJunos Router
    - user: admin
    - password: pass01

## Getting disk image for Paragon 2.4.1
As for the current version of Paragon Automation platform, version 2.4.1, the disk image is as only available as OVA package.

To install paragon virtual appliance on vmm, it requires the disk image, in VMDK or QCOW format.

so you need to extract the disk image from the OVA package, and put it into your home directory.

the challenge is the size of the disk image is 20G++, so you need to ensure that your VMM account has enough quota on the VMM directory.

you can copy the disk image from my home directory on VMM /vmm/data/user_disks/irzan/images 


## Deploying paragon 2.4.1 lab topology and initial configuration of VMs

1. Go to directory [Paragon Lab](./)
2. link file [lab_pa2.yaml](./lab_pa2.yaml) to file [lab.yaml](./lab.yaml)
3. Edit file [lab.yaml](./lab.yaml). Set the following parameters to choose which vmm server that you are going to use and the login credential:
    - vmmserver 
    - jumpserver
    - user 
    - adpassword
    - ssh_key_name ( please select the ssh key that you want to use, if you don't have it, create one using ssh-keygen and put it under directory **~/.ssh/** on your workstation )
3. If you want to add devices or change the topooogy of the lab, then edit file [lab.yaml](lab.yaml)
4. use [vmm.py](../../vmm.py) script to deploy the topology into the VMM. Run the following command from terminal

        ../../vmm.py upload  <-- to create the topology file and the configuration for the VMs and upload them into vmm server
        ../../vmm.py start   <-- to start the topology in the vmm server

5. Verify that you can access node **gw** using ssh (username: ubuntu,  password: pass01 ). You may have to wait for few minutes for node **gw** to be up and running
6. Run script [vmm.py](../../vmm.py) to send and run initial configuration on node **gw**. This will configure ip address on other interfaces (such ase eth1, eth2, etc) and enable dhcp server on node gw

        ../../vmm.py set_gw
7. Run script [vmm.py](../../vmm.py) to send and run initial configuration on node **crpd**, **client**, **br1**, **br2**, and **br3***. this will configure ip address on those nodes

        ../../vmm.py set_host

## update and upgrade package on node GW
1. open ssh session to node GW
2. update and upgrade package on node GW

        ssh gw
        sudo apt -y update && sudo apt -y upgrade
        sudo reboot

3. Wait until it rebooted.

## configure wireguard
The following step is to setup wireguard to allow direct access into the lab, for example to access the paragon dashboard directly

1. Install wireguard into your workstation

        brew install wireguard-tool  # this for macosx

2. on your workstation, run the following script

        ../../vmm.py get_wg_config

3. It will create configuration file for wireguard

        tmp/wg0_ws.conf : this configuration file is for your workstaiton
        tmp/wg0_gw.conf : this configuration file is for node **gw**


4. upload file wg0_gw.conf into node **gw** and run wireguard on node **gw**

        scp tmp/wg0_gw.conf gw:~/wg0.conf
        ssh gw "sudo cp wg0.conf /etc/wireguard/wg0.conf ; sudo systemctl enable wg-quick@wg0; sudo systemctl start wg-quick@wg0"

4. On your workstation, copy configuration file wg0_ws.conf into the wireguard local directory 

        cp tmp/wg0_ws.conf /usr/local/etc/wireguard/wg0.conf

7. on your workstation, start wireguard session, and test connectivity to the lab

        sudo wg-quick up wg0
        ping 172.16.11.254


## configure BGP on node **gw**

1. on node **gw**, access console for frr

       sudo vtysh 

2. put this configuration into FRR

       config t
       router bgp 65100
       no bgp ebgp-requires-policy
       neighbor 172.16.11.11 remote-as 65101
       neighbor 172.16.11.12 remote-as 65101
       neighbor 172.16.11.13 remote-as 65101
       neighbor 172.16.11.14 remote-as 65101
       exit
       !
       end
       write mem

## set ip address on Paragon virtual appliance
1. To access graphic console of Paragon virtual appliance using VNC, open ssh session to node **gw**, and the login banner will provide the URL to access VNC port of node1, node2, node2, node3

        ----------------------------------------------
        To access console of VM, use the following URL
        ----------------------------------------------
        console node1 : http://10.49.1.171:6081/vnc.html
        console node2 : http://10.49.1.171:6082/vnc.html
        console node3 : http://10.49.1.171:6083/vnc.html
        console node4 : http://10.49.1.171:6084/vnc.html

2. on node **gw**, run the script to start web proxy to access the vnc port

        /usr/local/bin/start_vnc.sh

3. To configure node1, on web browser of your workstation open session to url of node1

        http://10.49.1.171:6081/vnc.html

     ![connect_to_vnc.jpg](images/connect_to_vnc.jpg)
     
4. Click connect to open VNC connection to node1

5. Set the password, hostname, and ip address of node1

6. Use the following table to set ip address on the nodes. DNS 10.49.32.95/97 are internal DNS server. it is requires to be able to access ntp.juniper.net (the internal NTP server)

node | ip address | gateway | dns1 | dns2
-|-|-|-|-
node1|172.16.11.11/24|172.16.11.254|10.49.32.95|10.49.32.97
node2|172.16.11.12/24|172.16.11.254|10.49.32.95|10.49.32.97
node3|172.16.11.13/24|172.16.11.254|10.49.32.95|10.49.32.97
node4|172.16.11.14/24|172.16.11.254|10.49.32.95|10.49.32.97

7. Exit from the CLI, but don't create the cluster... just exit, and test connectivity to 172.16.11.254
8. Repat step 4 to 7 for node2, node3, and node4


## create paragon cluster
1. From your workstation, open ssh session into node1, and you will enter paragon shell

        ssh node1

2. Enter the following configuration on paragon shell. change the web-admin-user to your email

       configure
       set paragon cluster nodes kubernetes 1 address 172.16.11.11
       set paragon cluster nodes kubernetes 2 address 172.16.11.12
       set paragon cluster nodes kubernetes 3 address 172.16.11.13
       set paragon cluster nodes kubernetes 4 address 172.16.11.14
       set paragon cluster ntp ntp-servers ntp.juniper.net
       set paragon cluster common-services ingress ingress-vip 172.16.12.1
       set paragon cluster applications active-assurance test-agent-gateway-vip 172.16.12.2
       set paragon cluster applications web-ui web-admin-user "irzan@juniper.net"   
       set paragon cluster applications web-ui web-admin-password "J4k4rt4#170845" 
       set paragon cluster applications pathfinder pce-server pce-server-vip 172.16.12.3
       set paragon cluster install enable-l3-vip true
       set paragon cluster common-services metallb metallb-bgp-peer peer-ip 172.16.11.254 peer-asn 65100 local-asn 65101 local-nodes 172.16.11.11 
       set paragon cluster common-services metallb metallb-bgp-peer peer-ip 172.16.11.254 peer-asn 65100 local-asn 65101 local-nodes 172.16.11.12
       set paragon cluster common-services metallb metallb-bgp-peer peer-ip 172.16.11.254 peer-asn 65100 local-asn 65101 local-nodes 172.16.11.13  
       set paragon cluster common-services metallb metallb-bgp-peer peer-ip 172.16.11.254 peer-asn 65100 local-asn 65101 local-nodes 172.16.11.14
       commit
       exit

       # optioanl
       # set paragon cluster applications routingbot routingbot-crpd-vip 172.16.12.4
       # set paragon cluster applications aiops install-aiml true
       # set paragon cluster applications aiops enable-device-health true


3. Create the configuration file by running this command on paragon shell

        request paragon config

4. Create ssh-key to allow access between nodes. Use user **root** and the password that you setup on the node initialization

        request paragon ssh-key

5. Start deploying cluster

        request paragon deploy cluster input "-e ignore_iops_check=yes"

6. It will take around 60minutes ++ for paragon cluster deployment
7. The installation progress can be monitored using this command

        monitor start /epic/config/log
8. or from the linux shell, run the following command

        tail -f /root/epic/config/log
    
    ![pa2_done](./images/pa2_done.jpg)

9. Once the cluster is done, exit from the Paragon shell, and login again to finish the installation

    ![pa2_finish](./images/pa2_finish.jpg)

10. Now the paragon 2.4.1 cluster is installed.


## access the web dashboard of Paragon appliance
1. verify that wireguard session is up and running

        sudo wg show 

2. access [web dashboard of Paragaon automation ](https://172.16.12.1)
3. Login using the username (email addressess) and password that was configured during cluster deployment.

## preparing node crpd, client, and others

1. go to directoy [config/linux_node](config/linux_node/)
2. Run ansibple playbook [update_system.yaml](config/linux_node/update_system.yaml)

        cd config/linux_node
        ansible-playbook update_system.yaml

3. the playbook will install update into node **crpd**, **client**

## install cRPD on node crpd to run is as Route reflector
1. upload file [install_crpd.sh](../../install_crpd.sh) into node **crpd**

        scp ../../install_crpd.sh crpd:~/

2. open ssh session into node **crpd**
3. Download Juniper cRPD into node **crpd**
4. Load cRPD image on node **crpd**

        sudo podman load -i junos-routing-crpd-docker-amd64-24.4R1.9.tgz

5. start cRPD container on node **crpd**

        ./install_crdp.sh localhost/crpd:24.4R1.9

5. verify that cRPD is up and running

        sudo podman ps -a

6. Access cRPD cli

        sudo podman exec -it crpd cli

7. Enter the following configuration into cRPD

       set interfaces lo0 unit 0 family inet address 10.100.255.20/32
       set interfaces lo0 unit 0 family iso address 49.0001.0001.0001.0020.00
       set routing-options rib inet.3 static route 0.0.0.0/0 discard
       set routing-options autonomous-system 65200
       set protocols bgp group to_client type internal
       set protocols bgp group to_client passive
       set protocols bgp group to_client family inet-vpn unicast
       set protocols bgp group to_client family inet6-vpn unicast
       set protocols bgp group to_client family evpn signaling
       set protocols bgp group to_client cluster 10.100.255.20
       set protocols bgp group to_client allow 10.100.255.0/24
       set protocols isis interface eth1 level 1 disable
       set protocols isis interface eth1 point-to-point
       set protocols isis interface lo0.0 level 1 disable
       set protocols isis interface lo0.0 passive
       set protocols isis level 2 authentication-key "$9$H.fQ69A0BE9CK8LxsYTzF/9AtuO1Ec"
       set protocols isis level 2 authentication-type md5


## load configuration for vJunosRouter

1. Currently, all the vJunosRouter nodes (PE1, PE2, PE3, PE4, P1, P2, P3, P4, P5) has been loaded with initial configuration (such as ip addresses on interfaces, routing protocol and MPLS forwarding). You can verify it to by login into one of the vJunosRouter node, and check the configuration

2. Next, additional configuration will be loaded, to allow IPv4 of the loopback on vJunosRouter to be accessible from the Paragon Server.

3. Go to directory [config/router](config/router/)


5. Run ansible playbook [config/router/update_router.yaml](config/router/update_router.yaml) to upload configuration into vJunosRouter node

        ansible-playbook update_router.yaml

6. On cRPD, verify that BGP peer to vJunosRouter are up

        ssh crpd
        sudo podman exec -it crpd1 cli
        show bgp summary

7. From node **gw**, test connectivity to loopback for vJunosRouter (for exampe 10.100.255.1, 10.100.255.2, 10.100.255.3)

        ping 10.100.255.1
        ssh admin@10.100.255.1





## Lab Exercise
Now you can start exploring Juniper Paragon 2.0.0

you can use the following [document](pa_2.0.0/LabExercise.md) as guideline 

## start and stop 


