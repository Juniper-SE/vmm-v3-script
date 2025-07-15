# Running Juniper Apstra 5.0 and vJunosSwitch
this script is to run Juniper Apstra 5.0, Apstra ZTP server and vJunosSwitch (21.2R3-S1.7) on juniper's VMM

## Topology
The logical topology of the testbed is as follows :
![topology](images/topology1.png)

### DC1
![topology](images/topology2.png)

### DC2
![topology](images/topology3.png)

### DC3
![topology](images/topology4.png)


## Devices in the lab

- DC1:
    - spine : Spine1, Spine2 (vJunosSwitch)
    - leaf : leaf1, leaf2, leaf3, leaf4, leaf5, leaf6 (vJunosSwitch)
    - BMS : svr1, svr2, svr3, svr4,  (linux())
    - BMS with hypervisor (KVM) : svr5, lxc1, lxc2 (linux)
- DC2
    - collapsed switches: sw1, sw2 (vJunosSwitch)
    - BMS : svr6, svr7 (linux)
    - BMS with hypervisor (KVM) :  lxc3, lxc4 (linux)
- DC3:
    - spine : Spine1, Spine2 (vJunosSwitch)
    - leaf : leaf1, leaf2, leaf3, leaf4 (vJunosSwitch)
    - BMS : svr8, svr9 (linux())
    - BMS with hypervisor (KVM) : lxc5, lxc6 (linux)
- External
    - ext : external router (VMX)
    - fw1 : firewall (vSRX)
    - BMS : svr10, srv20 ,  (linux)
    - GW: Linux router that provide connection to internet
    - vxlangw   
- IP/Wan Backbone :
    - Router : PE1, PE2, P1 (vJunosRouter )
- Apstra
    - Juniper Apstra 4.2.2
    - ZTP server 4.2.2
## Device Connectivity


## Credential to access devices
- Ubuntu linux
    - user: ubuntu
    - password: pass01
- Alpine linux
    - user: ubuntu
    - password: pass01
- vJunosRouter and vSRX
    - user: admin
    - password: admin
- vJunosSwitch
    - user: aosadmin
    - password: aosadmin123

# To create the lab topology and initial configuration of VMs
1. Go to directory [dc_with_vjunos](./)
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

5. Verify that you can access node **gw** using ssh (username: ubuntu,  password: pass01 ). You may have to wait for few minutes for node **gw** to be up and running
6. Run script [vmm.py](../../vmm.py) to send and run initial configuration on node **gw**

        ../../vmm.py set_gw

7. Run script [vmm.py](../../vmm.py) to send and run initial configuration on linux nodes. This script will also reboot the VM. So wait before you test connectivity into the VM

        ../../vmm.py set_host

8. Run script [vmm.py](../../vmm.py) to get the list of mac address for all vjunos-switch devices.

        ../../vmm.py get_vjunos_mac 

8. Run script [vmm.py](../../vmm.py) to create wireguard configuration

        ../../vmm.py get_wg_config

9. upload file tmp/wg0_gw.conf into node **gw**, and move file tmp/wg0_ws.conf into your workstation wireguard directory
10. Open ssh session into node **gw**, copy file wg0_gw.conf into /etc/wireguard/wg0.conf and start wireguard service

        sudo systemctl enable wg-quick@wg0
        sudo systemctl start wg-quick@wg0

11. go into directory linux_node, and run ansible playbook update_system

        ansible-playbook update_system.yaml

12. on your workstation, start wireguard connection to node **gw**, and verify that you can reach 172.16.55.254


## Setup Juniper Apstra
1. Apstra nodes will be assigned with the following ip address

    node | ip address
    --|------
    controller| 172.16.55.1
    worker1| 172.16.55.2
    worker2| 172.16.55.3
    ztp| 172.16.55.4
    apstra flow: 172.16.55.5

2. From your workstation open ssh session to node controller, login using default user/password, and do the following things
    - change password
    - set ip address to static (use the same ip address settings)
    - set Web UI password

3. drop to shell, create directory ~/.ssh, and download ssh key from node **gw**

        mkdir ~/.ssh
        scp ubuntu@172.16.55.254:~/.ssh/* .ssh/

4. Repeat step 2 and 3 for node worker1 and worker2
5. Open ssh to node ztp, login using default username/password, and to the following things
    - change password
    - set ip address to static (use the same ip address settings)
6. drop to shell, create directory ~/.ssh, and download ssh key from node **gw**

        mkdir ~/.ssh
        scp ubuntu@172.16.55.254:~/.ssh/* .ssh/
7. open ssh to node apstra flow, login using default username/password, and edit file /etc/netplan/01-netcfg.yaml, and set the ip address to static

        sudo vi /etc/netplan/01-netcfg.yaml
    
        # This is the network config written by 'subiquity'
        network:
        ethernets:
            eth0:
            dhcp4: false
            addresses:
            - 172.16.55.5/24
            gateway4: 172.16.55.254
            nameservers:
                addresses:
                - 10.49.32.95
                - 10.49.32.97
            #  search: []
        version: 2

8. run "sudo netplan apply" to apply network configuration
9. drop to shell, create directory ~/.ssh, and download ssh key from node **gw**

        mkdir ~/.ssh
        scp ubuntu@172.16.55.254:~/.ssh/* .ssh/

## Accesing Apstra Web UI
there are three options to access Web UI of AOS.
1. Using wireguard VPN
2. using sock proxy with SSH dynamic forwarding
3. Using ssh forwarding

## Accessing Apstra Web UI using wireguard VPN
1. on your workstation, install wiregauard vpn 

        brew install wireguard-go

2. If wireguard configuration has not been created, then create it using vmm.py script

        ../../vmm.py create_wg_config

3. it will create to configuration file, tmp/wg0_ws.conf which is the wireguard configuration for your workstation, and tmp/wg0_gw.conf, which is the wireguard configuration for node gw

4. upload file tmp/wg0_gw.conf into node gw, put it into file /etc/wireguard/wg0.conf, and start wireguard services

        scp tmp/wg0_gw.conf gw:~/
        ssh gw "sudo cp ~/wg0_gw.conf /etc/wireguard/wg0.conf"
        ssh gw "sudo wg-quick up wg0"

5. copy file tmp/wg0_ws.conf into your workstation wireguard directory

        cp tmp/wg0_ws.conf /usr/local/etc/wireguard/wg0.conf
        sudo wg-quick up wg0

6. Verify that from your workstation you can access apstra controller

        ping 172.16.55.1
        curl -k https://172.16.55.1
        
7. open dashboard of apstra controller

        https://172.16.55.1

## Accessing Apstra WEB UI using sock proxy with SSH dynamic forwarding
1. from your workstation, open ssh session to node **proxy** and keep the session open

        ssh proxy

2. Use firefox web browser, open setting configuration, and search for proxy configuration.
3. Under **Configure Proxy Access to the Internet**, and set to **Manual proxy configuratio**
4. under **SOCKS Host** set ip address to **127.0.0.1** and Port to **1080**, and clik **OK** to save it
5. on the URL bar, open access to apstra dashboard https://172.16.55.1

![firefox](images/firefox_proxy.jpg)


## Accessing Apstra WEB UI using ssh forwarding
1. open ssh session with forwarding to ip address of apstra server (172.16.10.2) and port 443

        ssh -L 9191:172.16.55.1:443 gw

2. from webbrowser on your workstation, open https session to https://127.0.0.1:9191


## add license into apstra controller
1. open Web UI of apstra controller
2. from menu, select Platform > Licenses, and click create license to add the new license


## add worker nodes into apstra controller
1. Open Web UI of apstra controller
2. From menu, select Platform > Apstra Clusers, and click create node, and add the following node. use username admin

    nodes|address| tag
    -|-|-
    apstraw2|172.16.55.2|iba, offbox
    apstraw3|172.16.55.3|iba, offbox

3. Edit node controller, and remove all the tags


## add ZTP into apstra controller
1. open Web UI of apstra controller
2. From menu, select Platform > User, and create one user with the following parameter

    - username : ztp
    - password: J4k4rt4#01
    - global role: device_ztp
3. Open Web UI of Apstra ZTP, use default username/password, and change the password
4. Connect ZTP to apstra controller using the following parameters
    - Apstra address: 172.16.55.1
    - username : ztp
    - password: <password>

5. on apstra controller Web UI, from menu, select Devices > Services, to verify that apstra ZTP has established connection to Apstra controller



## Configure the network
1. upload crpd image into node **crpd**

        scp junos-routing-crpd-docker-amd64-24.2R1.14.tgz crpd:~/
2. load crpd image using podman

        sudo podman load -i junos-routing-crpd-docker-amd64-24.2R1.14.tgz
        sudo podman image ls

3. Create two volume 

        export CRPD_NAME=crpd1
        sudo podman volume create ${CRPD_NAME}-config
        sudo podman volume create ${CRPD_NAME}-varlog
4. Run the crpd

        export CRPD_NAME=crpd1
        sudo podman run --rm --detach --name ${CRPD_NAME} -h ${CRPD_NAME} \
            --net=host --privileged \
            -v ${CRPD_NAME}-config:/config \
            -v ${CRPD_NAME}-varlog:/var/log \
            -it localhost/crpd:24.2R1.14

5. Access 


## Configure device profile (vjunos and vjunos_evolved)
if Apstra 4.1.2 is and vjunos version 23.X is used, then the following steps are needed (on Apstra 4.1.2, by default the device profile is configured for junos/junosEVO up to version 22.X)

1. On Apstra Dashboard, click **Device** > **Device Profiles**

   ![apstra1](images/apstra1.jpg)

2. Search for vJunosSwitch, and clone it

   ![apstra2](images/apstra2.jpg)
3. Set a new name, for example *Juniper vJunosSwitch 23.X"

   ![apstra3](images/apstra3.jpg)
4. Click on selector, and edit field Version, change it from (1[89]|2[0-2])\..* to (1[89]|2[0-3])\..* 
5. Click **Clone** to save it.
   
   ![apstra4](images/apstra4.jpg)

The following steps is required to create customized device profile for vjunos evolved

1. On Apstra Dashboard, click **Device** > **Device Profiles**

   ![apstra1](images/apstra1.jpg)

2. Search for PTX

   ![apstra2](images/apstra5.jpg)

3. Clone **Juniper_PTX10001-36MR** and set a new name, for example *vJunosEvolved"

   ![apstra3](images/apstra6.jpg)
4. Click on **Selector**, and edit field Version, change it from (20\.[34].*|2[12]\..*)-EVO$ to (20\.[34].*|2[123]\..*)-EVO$
   ![apstra4](images/apstra7.jpg)
5. Click on **Port**, and delete the existing panel
6. Clic **add panel** and create 12 ports panel
7. Select all port (port 1 to 12)
8. Decrement **the Display ID** by 1 (by click negative sign)
9. Set connector type to SFP+
10. Click **add new transformation**:
   - set **speed** : 10G
   - set **Name template** : et-0/0/<port_id>
11. Click **add transformation**
12. Click **Clone** to save it.
   

   (1[89]|2[0-3])\..*


## Upload configuration into node PE1, PE2, PE3 and P1

1. router PE1, PE2, PE3, and P1 must be configured to allow ztp/dhcp traffic forwarded between DC1, DC2, DC3 and apstra management network.
2. To upload configuration, use ansible script [upload_config.yaml](router/upload_config.yaml)

        cd config/router
        ansible-playbook upload_config.yaml

3. Now routers are configured, and vJunosSwitch will go through the ZTP process.

4. On Apstra UI Dashboard, go to **Devices**>**ZTP Status**>**Devices**, to verify that network devices (swithes) are discovered through ZTP

    ![ztp16](images/ztp16.png)

5. Wait until the **ZTP status** is **completed**

    ![ztp17](images/ztp17.png)


## Lab exercise

You can refer to [this document](LabExercise/README.md) for lab exercise



