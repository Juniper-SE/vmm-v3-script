# How setup Paragon 2.4.0 Lab on VMM
## topology

![topology](images/topology_lab.jpg)

## note
Tested with paragon automation 2.4.0
based on this [documentation](https://www.juniper.net/documentation/us/en/software/juniper-paragon-automation2.4.0/installation-guide/index.html).

## Devices in the lab

- vJunosRouter : pe11, pe12, pe13, pe14, pe15 p1, p2, p3, p4, pe5
- Linux client: client (to provide test traffic) (linux ubuntu)
- Bridge : br1, br2, br3 , br4( linux bridge between junos node to simulate link failure, delay and packet loss) (linux alpine)

- Kubernetes cluster for Paragon Automation
    - Node1, Node2, Node3, Node4 : Paragon 2.4.0 Virtual Appliance


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

## Getting disk image for Paragon 2.4.0
As for the current version of Paragon Automation platform, version 2.4.0, the disk image is as only available as OVA package.

To install paragon virtual appliance on vmm, it requires the disk image, in VMDK or QCOW format.

so you need to extract the disk image from the OVA package, and put it into your home directory.

the challenge is the size of the disk image is 20G++, so you need to ensure that your VMM account has enough quota on the VMM directory.

you can copy the disk image from my home directory on VMM /vmm/data/user_disks/irzan/images 


## Deploying paragon 2.4.0 lab topology and initial configuration of VMs

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

## update and upgrade package on node GW
1. open ssh session to node GW
2. update and upgrade package on node GW

        ssh gw
        sudo apt -y update && sudo apt -y upgrade
        sudo reboot

3. Wait until it rebooted.

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


## configure wireguard
The following step is to setup wireguard to allow direct access into the lab, for example to access the paragon dashboard directly

1. Install wireguard into your workstation

        brew install wireguard-tool  # this for macosx

2. on your workstation, run the following script

        ../../vmm.py get_wg_config

3. It will create configuration file for wireguard

        tmp/wg0_ws.conf : this configuration file is for your workstaiton
        tmp/wg0_gw.conf : this configuration file is for node **gw**


4. upload file wg0_gw.conf into node **gw** and run wireguard on node **gw)**

        scp tmp/wg0_gw.conf gw:~/wg0.conf
        ssh gw "sudo cp wg0.conf /etc/wireguard/wg0.conf ; sudo wg-quick up wg0"

4. copy configuration file wg0_ws.conf into the wireguard local directory 

        cp tmp/wg0_ws.conf /usr/local/etc/wireguard/wg0.conf

7. on your workstation, start wireguard session, and test connectivity to the lab

        sudo wg-quick up wg0
        ping 172.16.11.11
        ssh root@172.16.11.11

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
       set paragon cluster applications routingbot routingbot-crpd-vip 172.16.12.4
       set paragon cluster applications aiops install-aiml true
       set paragon cluster applications aiops enable-device-health true
       set paragon cluster install enable-l3-vip true
       set paragon cluster common-services metallb metallb-bgp-peer peer-ip 172.16.11.254 peer-asn 65100 local-asn 65101 local-nodes 172.16.11.11 
       set paragon cluster common-services metallb metallb-bgp-peer peer-ip 172.16.11.254 peer-asn 65100 local-asn 65101 local-nodes 172.16.11.12
       set paragon cluster common-services metallb metallb-bgp-peer peer-ip 172.16.11.254 peer-asn 65100 local-asn 65101 local-nodes 172.16.11.13  
       set paragon cluster common-services metallb metallb-bgp-peer peer-ip 172.16.11.254 peer-asn 65100 local-asn 65101 local-nodes 172.16.11.14
       commit
       exit


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

10. Now the paragon 2.4.0 cluster is installed.


## access the web dashboard of Paragon appliance
1. verify that wireguard session is up and running

        sudo wg show 

2. access [web dashboard of Paragaon automation ](https://172.16.12.1)
3. Login using the username (email addressess) and password that was configured during cluster deployment.


## Deploying lab topology (routers) and initial configuration of VMs

1. Go to directory [Paragon Lab](./)
2. link file [lab_pa2_router.yaml](./lab_pa2_router.yaml) to file [lab.yaml](./lab.yaml)
3. Edit file [lab.yaml](./lab.yaml). Set the following parameters to choose which vmm server that you are going to use and the login credential:
    - vmmserver 
    - jumpserver
    - user 
    - adpassword
    - ssh_key_name ( please select the ssh key that you want to use, if you don't have it, create one using ssh-keygen and put it under directory **~/.ssh/** on your workstation )

    PLEASE MAKE SURE THAT **vmmserver** configuration of file [lab_pa2_router.yaml](./lab_pa2_router.yaml) is different from [lab_pa2.yaml](./lab_pa2.yaml).. otherwise the paragon nodes that has been deployed will be destroyed.
    
3. If you want to add devices or change the topooogy of the lab, then edit file [lab.yaml](lab.yaml)
4. use [vmm.py](../../vmm.py) script to deploy the topology into the VMM. Run the following command from terminal

        ../../vmm.py upload  <-- to create the topology file and the configuration for the VMs and upload them into vmm server
        ../../vmm.py start   <-- to start the topology in the vmm server

5. Verify that you can access node **gw** using ssh (username: ubuntu,  password: pass01 ). You may have to wait for few minutes for node **gw** to be up and running
6. Run script [vmm.py](../../vmm.py) to send and run initial configuration on node **gw**. This will configure ip address on other interfaces (such ase eth1, eth2, etc) and enable dhcp server on node gw

        ../../vmm.py set_gw

7. Run script [vmm.py](../../vmm.py) to send and run initial configuration on node **gw**. This will configure ip address on other interfaces (such ase eth1, eth2, etc) and enable dhcp server on node gw

        ../../vmm.py set_gw


## preparing node crpd, client, and others

1. go to directoy [config/linuxnode](config/linuxnode/)
2. Run ansibple playbook [update_system.yaml](config/linuxnode/update_system.yaml)

        cd config/linuxnode
        ansible-playbook update_system.yaml

3. the playbook will install update into node **crpd**, **client**

## install cRPD on node crpd to run is as Route reflector
1. open ssh session into node **crpd**
2. install podman and cri-o, using the following script

        export CRIO_VERSION=v1.30
        curl -fsSL https://pkgs.k8s.io/addons:/cri-o:/stable:/$CRIO_VERSION/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/cri-o-apt-keyring.gpg
        echo "deb [signed-by=/etc/apt/keyrings/cri-o-apt-keyring.gpg] https://pkgs.k8s.io/addons:/cri-o:/stable:/$CRIO_VERSION/deb/ /" | sudo tee /etc/apt/sources.list.d/cri-o.list

        sudo apt -y update
        sudo apt -y upgrade
        sudo apt install -y cri-o podman lldpd
        sudo systemctl start crio.service

3. Upload crpd image into node crpd

        scp junos-routing-crpd-docker-amd64-24.2R1.14.tgz crpd:~/

4. Load crpd image using podman

        sudo podman load -i junos-routing-crpd-docker-amd64-24.2R1.14.tgz
        sudo podman image ls

5. Create volumes required by crpd

        export CRPD_NAME=crpd1
        sudo podman volume create ${CRPD_NAME}-config
        sudo podman volume create ${CRPD_NAME}-varlog

6. Run the following script to start CRPD

        export CRPD_NAME=crpd1
        sudo podman run --rm --detach --name ${CRPD_NAME} -h ${CRPD_NAME} \
          --net=host --privileged \
          -v ${CRPD_NAME}-config:/config \
          -v ${CRPD_NAME}-varlog:/var/log \
          -it localhost/crpd:24.2R1.14
        sudo podman ps -a

6. Load the initial configuration for crpd, [crpd.set](config/router/initial_config/crpd.set), and commit the configuration

        sudo podman exec -it crpd1 cli

## load configuration for vJunosRouter

1. Currently, all the vJunosRouter nodes (PE11, PE12, PE13, PE14, PE15, P1, P2, P3, P4, P5) has been loaded with initial configuration and enable SRv6. you can verify it to by login into one of the vJunosRouter node, and check the configuration
2. Next, additional configuration will be loaded, to allow IPv4 of the loopback on vJunosRouter to be accessible from the Paragon Server.
3. Go to directory [config/router](config/router/)

4. Edit file  [config/router/update_router.yaml](config/router/update_router.yaml), and verify than under "vars:", variable "conf_dir:" is set to "./initial_config"

        ---
        - name: configure SRv6 and IPv6 on routers
          hosts:
          - all
          roles:
          - juniper.junos
          vars:
            username: admin
            conf_dir: "./initial_config"
            conf_file: "{{ conf_dir }}/{{ inventory_hostname }}.set"
          connection: local
          gather_facts: no
          tasks:
          - name: upload config into router
            juniper_junos_config:
                host: "{{ ansible_host }}"
                user: "{{ username }}"
                file: "{{ conf_file}}"
                config_mode: "exclusive"
                load: "set"

5. Run ansible playbook [config/router/update_router.yaml](config/router/update_router.yaml) to upload configuration into vJunosRouter node

        ansible-playbook update_router.yaml

6. On cRPD, verify that BGP peer to vJunosRouter are up

        ssh crpd
        sudo podman exec -it crpd1 cli
        show bgp summary
7. From node **gw**, test connectivity to loopback for vJunosRouter (for exampe 192.168.255.201, 192.168.255.211)

        ping 192.168.255.201
        ssh admin@192.168.255.201
        ping 192.168.255.211
        ssh admin@192.168.255.211

## configure client for site1, site2, site3, site4
there are four sites in the lab, site1 connected to pe11, site2 connected to pe12, site3 connected to pe13, and site4 connected to pe14.

The following steps, we are going to configure clients for site1, site2, site3, and site4. 

The client is using linux container (LXC) running on node **client**

1. open ssh session into node **client**
2. Refresh snap

        sudo snap refresh

3. Initialize LXD

        sudo lxd init

4. Download alpine linux LXC image

        lxc image copy images:alpine/edge local: --alias alpine
        lxc image ls

5. Create two LXC instance

        lxc launch alpine router
        lxc launch alpine client

6. Access LXC client shell, install openssh, add sshd to startup script, and create ssh-key for ssh

        lxc exec client sh
        apk update
        apk upgrade
        apk add openssh
        rc-update add sshd
        service sshd start
        ssh-keygen -t rsa
        cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys
        exit
        lxc stop client

7. Access LXC router shell, install frr, dhcp-server and lldpd, add dhcpd and frr to startup script

        lxc exec router sh
        apk update
        apk upgrade
        apk add frr dhcp-server lldpd
        rc-update add dhcpd
        rc-update add frr
        sed -i -e "s/bgpd=no/bgpd=yes/" /etc/frr/daemons
        exit
        lxc stop router
        lxc ls

8. from your workstation, upload scripts [config/client/lxc/create/set_network.sh](config/client/lxc_create/set_network.sh) script [config/client/lxc_create/create_lxc_routing_global.sh](config/client/lxc_create/create_lxc_routing_global.sh) to node **client**, and run those script on node **client**

        scp config/client/lxc_create/create_lxc_routing_global.sh client:~/
        scp config/client/lxc/create/set_network.sh client:~/
        ssh client
        ./set_network.sh
        ./create_lxc_routing_global.sh

9. Multiple LXC instances has been create, and they can be used to test connectivity between sites.






## Lab Exercise
Now you can start exploring Juniper Paragon 2.0.0

you can use the following [document](pa_2.0.0/LabExercise.md) as guideline 


