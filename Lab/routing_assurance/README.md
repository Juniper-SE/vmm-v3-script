# How setup Routing Assurance Lab
## topology

![topology](topology.webp)


for topology, it consists of the following:
- vJunos-Router: PE1, PE2, PE3, PE4, PE5, P1, P2, P3, P4, P5
- linux VM to run cRPD: crpd
- Linux VM to simulate CE or subscriber's devices: client
- GW: gateway for connection to Juniper's Intranet

This documentation provides information on how to install and setup this lab.



## update and upgrade package on linux node

1. use ansible playbook [updates_nodes.yaml](host/update_nodes.yaml) to update and install software on node gw

        cd ~/git/vmm-v3-script/Lab/routing_director/RD/host
        ansible-playbook updates_node.yaml

2. Wait until they are rebooted.


## configure wireguard
The following step is to setup wireguard to allow direct access into the lab, for example to access the Routing Director dashboard directly from your workstation.

Wireguard is also used to provide connectivity to another VMM topology (lab network) where all the vJunos VMs are running.

Screenshot recording for this can be found [here](https://asciinema.org/a/741934)

1. Install wireguard into your workstation

        brew install wireguard-tool  # this for macosx

2. on your workstation, run the following script

        ../../../vmm.py get_wg_config

3. It will create configuration file for wireguard

        tmp/wg0_ws.conf : this configuration file is for your workstaiton
        tmp/wg0_gw.conf : this configuration file is for node **gw**


4. upload file wg0_gw.conf into node **gw** and run wireguard on node **gw**

        scp tmp/wg0_gw.conf gw:~/wg0.conf
        ssh gw "sudo cp wg0.conf /etc/wireguard/wg0.conf ; sudo systemctl enable wg-quick@wg0; sudo systemctl start wg-quick@wg0"

4. On your workstation, copy configuration file wg0_ws.conf into the wireguard local directory 

        sudo cp tmp/wg0_ws.conf /usr/local/etc/wireguard/wg0.conf

7. on your workstation, start wireguard session, and test connectivity to the lab

        sudo wg-quick up wg0
        ping 172.16.11.254
        ping 172.16.11.11
        ping 172.16.11.14

## Deploying lab topology

Screenshot recording for this can be found [here]()

1. Go to directory [Lab/routing_assurance](./)
2. Edit file [lab.yaml](./lab.yaml). Set the following parameters to choose which vmm server that you are going to use and the login credential:
    - vmmserver 
    - user 
4. use [vmm.py](../../vmm.py) script to deploy the topology into the VMM. Run the following command from terminal

        ../../vmm.py upload  <-- to create the topology file and the configuration for the VMs and upload them into vmm server
        ../../vmm.py start   <-- to start the topology in the vmm server

5. Verify that you can access node **gw** using ssh (username: ubuntu,  password: pass01 ). You may have to wait for few minutes for node **gw** to be up and running
6. Run script [vmm.py](../../vmm.py) to send and run initial configuration on node **gw**. This will configure ip address on other interfaces (such ase eth1, eth2, etc), enable dhcp server and dns server on node gw

        ../../vmm.py set_gw

7. Run script [vmm.py](../../vmm.py) to send and run initial configuration on node **crpd**, **client**, **br1**, **br2**, **br3**. This will configure ip address on other interfaces (such ase eth1, eth2, etc), enable dhcp server and dns server on node gw

        ../../vmm.py set_host

8. use ansible playbook [updates_nodes.yaml](./setup/host/update_nodes.yaml) to update and install software on node gw

        cd ~/git/vmm-v3-script/Lab/routing_assurance/setup/host
        ansible-playbook updates_node.yaml

9. Wait until they are rebooted. 





## Lab Exercise
Now you can start exploring Routing Assurance

you can use the following [document](lab_exercise/README.md) as guideline 
