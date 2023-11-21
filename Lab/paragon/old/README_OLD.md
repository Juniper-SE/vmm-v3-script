# How setup the lab
## topology

![topology](images/topology_paragon.png)

## note
Tested with paragon automation version 21.1 and 21.2

for version 21.2, it requires ceph.

Based on the [documentation](https://www.juniper.net/documentation/us/en/software/paragon-automation21.2/paragon-automation-installation-guide/topics/concept/paragon-install-system-reqs.html#paragon-automation-system-requirements__section_disk-partitions), it requires unformatted partition or disk for ceph storage.

Therefore for paragon automation installation on Juniper VMM, I have created another image (ubuntu1804.img and ubuntu20.04.img), where it has one harddisk with the size of 400G, 300G has been allocated for base OS, and 100G is free unused disk space.


## Devices in the lab

- VMX : r1, r2, r3, r4, r5, r6, r7, and r8
- Linux client: c1 (to provide test traffic) (linux ubuntu)
- Bridge : br1 ( linux bridge between junos node to simulate link failure, delay and packet loss) (linux alpine)

- Kubernetes cluster for Paragon Automation
    - Control node : Linux, to run Paragon automation deployer (linux ubuntu)
    - Node0, Node1, Node2, Node3 : Linux, to run kubernetes cluster (linux ubuntu)

## Credential to access devices
- Ubuntu linux
    - user: ubuntu
    - password: pass01
- Alpine linux
    - user: ubuntu
    - password: pass01
- JUNOS VM
    - user: admin
    - password: pass01

## To create the lab topology and initial configuration of VMs
1. Go to directory [Paragon Lab](./)
2. Edit file [lab.yaml](./lab.yaml). Set the following parameters to choose which vmm server that you are going to use and the login credential:
    - vmmserver 
    - jumpserver
    - user 
    - adpassword
    - ssh_key_name ( please select the ssh key that you want to use, if you don't have it, create one using ssh-keygen and put it under directory **~/.ssh/** on your workstation )
3. If you want to add devices or change the topooogy of the lab, then edit file [lab.yaml](lab.yaml)
4. use [vmm.py](../../vmm.py) script to deploy the topology into the VMM. Run the following command from terminal

        ../../vmm.py upload  <-- to create the topology file and the configuration for the VMs and upload them into vmm server
        ../../vmm.py start   <-- to start the topology in the vmm server

5. Add the content of file [tmp/ssh_config](tmp/ssh_config) into your ssh config file, ~/.ssh/config. If you have run the previous lab, please remove entries on file ~/.ssh/config from the previous lab (Any entries after "### the following lines are added by vmm-v3-script" must be deleted)

        cat tmp/ssh_config >> ~/.ssh/config

6. Verify that you can access node **gw** using ssh (username: ubuntu,  password: pass01 ). You may have to wait for few minutes for node **gw** to be up and running
7. Run script [vmm.py](../../vmm.py) to send and run initial configuration on node **gw**

        ../../vmm.py set_gw

8. Verify that you can access other nodes (linux and junos VM), such **control**, **node**, **node1**, etc. Please use the credential to login.

        ssh control

9. Run script [vmm.py](../../vmm.py) to send and run initial configuration on linux nodes. This script will also reboot the VM. So wait before you test connectivity into the VM

        ../../vmm.py set_host

10. Verify that you can access linux and junos VMs, such **control**, **node**, **node1**, without entering the password. You may have to wait for few minutes for the nodes to be up and running

        ssh control
        ssh pe1
        ssh pe2

## Uploading Paragon Automation installation file
1. if you are going to install Paragon automation version 21.2 or later, then you need create an empy partition on **node1**, **node2**, and  **node3**. Use this script [create_hd_part.sh](install/create_hd_part.sh) on node1, node2 and node3 to create empty partition.

        #!/bin/bash
        sudo fdisk -l /dev/sda
        echo "n
        3


        w
        q
        " | sudo fdisk /dev/sda
        sudo fdisk -l /dev/sda

2. If you have paragon automation installation file, upload it into node **control** ( Caution: The size of the installation (as for version 21.1) is around 10G, so it may take time to upload the file into node **control** from your workstation

        scp Paragon21.1.tar.gz control:~/
3. Alternatively, you can upload the installation file from Juniper internal server. To upload file from internal server, do the following steps
4. open ssh session into node **vmm**

        ssh vmm
5. on node **vmm**, edit file ~/.ssh/config, for entry **Host gw**, change the user from **root** to **ubuntu**
6. add the following entry into file ~/.ssh/config

        host control
            user ubuntu
            ProxyCommand ssh -W 172.16.11.99:22 gw

    ![vmm_ssh_config](images/vmm_ssh_config.jpg)

7. The paragon automation installation file should be under directory /volume/download/docroot/software/pa/<version>
8. Upload the file into node **control**
    ![upload_software](images/upload_sw.png)

## Installing Paragon Automation software
Please refer to the [installation guide](https://www.juniper.net/documentation/en_US/paragon-automation21.1/information-products/pathway-pages/paragon-automation-installation-guide.html) for Paragon Automation software.


1. From your workstation, upload script [install_docker.sh](install/install_docker.sh), files [config.yml](install/config.yml), [inventory](install/inventory), [set1.sh](install/set1.sh) and [updat1.sh](install/update1.sh) into node **control**

        scp install/install_docker.sh control:~/
        scp install/config_21.2/config.yml control:~/
        scp install/config_21.2/inventory control:~/
       
2. From your workstation run script [install/update1.sh](install/update1.sh). It set and reboot  node1, node2 and node3. Please wait until those nodes are back online before continue with the next step

        cd install/
        ./update1.sh


3. Open ssh session into node **control** and run script **install_docker.sh** to install docker (to allow the script to keep running, even when the ssh session is disconnected, run **tmux** command before it). the script will reboot node **control** automatically. 

        ssh control
        tmux
        ./install_docker.sh


4. Once node **control** is back online, open ssh session into it.
6. Extract Paragon installation file 

         tar xpvfz Paragon21.1.tar.gz


7. Run file **run** from paragon installation file  to initialize configuration directory **configdir**

        chmod +x Paragon21.1/run 
        ./Paragon21.1/run -c configdir init

    ![extract.png](images/extract.png)

8. Run file **run** with option **conf**, to configure the installer, or copy file **inventory** and **config.yml** into directory **configdir**. These files, inventory dan config.yml, are from my setup.

        ./Paragon21.1/run -c configdir init

    or 

        cp inventory configdir/
        cp config.yml configdir/

9. File config.yml from my setup, has the following parameter 

parameter | value
-|-
metallb_address (IP address for loadbalancer)| 172.16.11.50-172.16.11.80
callback_vip | 172.16.11.50
northstar_web_hostname| 172.16.11.50
northstar_pceserver_vip|172.16.11.53
crpd_autonomous_system| 64500
crpd_neighbors | 172.16.11.4
healthbot_vip| 172.16.11.51
healthbot_snmp_proxy_vip| 172.16.11.52


10. Start Paragon automation installation process. The installation proccess may take up to 60 minutes to finish.

        tmux
        ./Paragon21.1/run -c configdir deploy
    
    ![deploy.png](images/deploy.png)

    ![finish.png](images/finish.png)

## Accessing Web Interface of Paragon automation
1. From your workstation, open ssh session to node **proxy** and keep this session open if you need to access the web dashboard of Paragon Automation platform

        ssh -f -N proxy 

2. If you are using Firefox as web browser, set proxy with the following parameters
    - manual proxy configuration
    - SOCKS host : 127.0.0.1
    - PORT : 1080
    - type: SOCKS v4    
    ![firefox_proxy](images/firefox_proxy.png)

3. If you are using Chrome as web browser, install extension Foxy Proxy and configure it with the following parameters
    - manual proxy configuration
    - SOCKS host : 127.0.0.1
    - PORT : 1080
    - type: SOCKS v4    
    ![chrome_proxy1](images/chrome_proxy1.png)
    ![chrome_proxy2](images/chrome_proxy2.png)

4. Open http session to https://172.16.11.50, and login using default credential, user/password: admin/Admin123!, and change the password  
![web1](images/web1.png) 
![web2](images/web2.png) 
![web3](images/web3.png) 

5. By default, no license is installed on Paragon Automation platform, and access to Paragon automation function, Pathfinder, Planner and Insight, are disabled. Get the license from [Agile Internal Licensing Portal](https://internal-license.juniper.net/nckt/)

![license1](images/license1.png)

6. Install the license into Paragon automation platform, then menu to access Paragon automation function, Pathfinder, Insight, and Planner, will be accessible

![license2](images/license2.png)

or you can use [this](install/paragon_automation.txt) 

7. To enable proxy on javaws to access access into Paragon Planner Desktop, from terminal run **javaws -viewer**, and set the proxy

![java_cp](images/java_cp.png)
![network_settings](images/network_settings.png)
![socks_proxy](images/socks_proxy.png)

7. Now you can explore the Paragon automation platform. You can start doing [initial setup](Initial_setup.md)

