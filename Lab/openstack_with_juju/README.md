# Deploying openstack using charm

this document provide guide on how to install openstack using charm, which is based on [this](https://docs.openstack.org/project-deploy-guide/charm-deployment-guide/latest/)

The [original documentation](https://docs.openstack.org/project-deploy-guide/charm-deployment-guide/latest/) deploys openstack on compute nodes which are  deployed using MAAS.

in this document, the compute nodes are already deployed with Ubuntu 22.04, therefore MAAS is no longer required, only Juju is used to deploy the openstack using charm.

## Deploying the topology on VMM

1. Go to directory [openstack_with_juju]](./)
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

9. Run script [vmm.py](../../vmm.py) to create wireguard configuration

        ../../vmm.py get_wg_config

10. Upload file tmp/wg0_gw.conf into node **gw**, copy it into wireguard directory, and start the wireguard service

        scp tmp/wg0_gw.conf gw:~/wg0.conf
        ssh gw
        sudo cp wg0.conf /etc/wireguard/
        sudo systemctl enable wg-quick@wg0
        sudo systemctl start wg-quick@wg0

11. On your workstation, copy file tmp/wg0_ws.conf into your local wireguard directory, start wireguard, and test connectivity to the lab

        cp tmp/wg0_ws.conf /usr/local/etc/wireguard/wg0.dc.conf
        sudo wg-quick up wg0.dc
        ssh ubuntu@192.168.199.0
        ping 172.16.11.1

12. run the ansible playbook [update_system.yaml](linux_node/update_system.yaml) to update and install the necessary application on various nodes in the lab (client, juju, node0, node1, node2, node3)

        cd linux_node/
        ansible-playbook update_system.yaml

13. run the ansible playbook [update_system.yaml](linux_node/update_system.yaml) to update and install the necessary application on various nodes in the lab (client, juju, node0, node1, node2, node3)

        cd linux_node/
        ansible-playbook update_hosts.yaml

14. Follow the steps on this document [deploy_openstack](./deploy_openstack.md)

## change the network configuration of node gw
1. open ssh session into node gw

        ssh gw

2. edit file /etc/netplan/01_net.yaml

        sudo /etc/netplan/02_net.yaml

3. change the configuration from 

       network:
         ethernets:
           eth1:
             addresses : ['172.16.11.1/24']
           eth2:
             addresses : ['172.16.12.1/24', 'fc00:dead:beef:a012::1/64']
             
4. to the following
  
       cat << EOF | sudo tee /etc/netplan/02_net.yaml
       network:
         ethernets:
           eth1:
             addresses : ['172.16.11.1/24']
           eth2:
             addresses : ['172.16.12.1/24', 'fc00:dead:beef:a012::1/64']
         vlans:
           eth1vlan111:
             addresses:
             - 192.168.111.1/24
             - fc00:dead:beef:a111::1/64
             link: eth1
             id: 111
           eth1vlan112:
             addresses:
             - 192.168.112.1/24
             - fc00:dead:beef:a112::1/64
             link: eth1
             id: 112
           eth1vlan113:
             addresses:
             - 192.168.113.1/24
             - fc00:dead:beef:a113::1/64
             link: eth1
             id: 113
       EOF

             



