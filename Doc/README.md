# How to use Juniper VMM

release 0.91
## Overview
This script is used to create configuration files, which will be used to create and run VMs (Virtual Machines) on Juniper's VMM infastructure.
The scripts has been modified to work with VMM 3.0 

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

Select the vmm server that has enough token required for your topology, and put this server name in lab topology file, lab.yaml. Remember to put the FQDN of the vmm server, which is the name of the pod name found from [https://vmm.englab.juniper.net/default_live](https://vmm.englab.juniper.net/default_live), and add suffix **-vmm.englab.juniper.net**  (like the following example)

        lab.yaml
        ---
        name: topo1
        pod:
          vmmserver: q-pod26-vmm.englab.juniper.net

        ...
        

## Prepare python3 virtual environment

1. Create python3 virtual environment to the script. 

       # Please use python3 version 3.12 or less... 
       # Python3 version 3.13 may have problem with ansible modules (related to paramiko modules)

       python3 -m venv ~/python3/vmmlab

       or

       /opt/homebrew/Cellar/python@3.12/3.12.11/bin/python3.12 -m venv ~/python3/vmmlab
       

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

## Step by Step guide on how to use the script

1. Create configuration file for the lab **lab.yaml**. Put this file under a directory inside directory Lab. You can refer to the sample under directory lab.

       cd ~/git/vmm-v3-script/Lab
       mkdir topo1
       cd topo1 
       vi lab.yaml

2. Run the script with argument `upload`, to upload the configuration files into VMM server. The script will ctreate the configurations under directory `./tmp`. Files inside these directory will be uploaded into VMM server. You have to run this script, while you are inside the lab directory, for example if your lab name is topo1, then your lab directory will be ~/git/vmm-v3-script/Lab/topo1, and file lab.yaml must be on this directory.

        ../../vmm.py upload

3. Run the script with argument `start`, to start the topology on VMM. Remember any active topology will be stop and destroyed. Remember to backup the configuration of any existing running topology

        ../../vmm.py start

4. Verify that node GW is up and running, by initiating ssh session into it. The username to access node GW is **ubuntu** and poassword is **pass01**

        ssh gw

5. Run the script with argument `set_gw`, to configure other interfaces of node gw (interface em1, em2, etc), upload ssh key and dhcp server configuration. Node **GW** will be acting as DHCP server and tftp (for ZTP) for on ubuntu/centos/vJunos VM in the topology

        ../../vmm.py set_gw


6. Run the script with argument `set_host`, to configure Linux VM, such has hostname, change interface configuration from dhcp to static, and upload ssh key.

        ../../vmm.py set_host

6. vJunos VM in the topology, such as vJunos-Router, vJunos-Switch, and vJunos-Evolved will be assigned with initial configuration using ZTP. the initial configuration for these vJunos VM are createed by the script during **../../vmm.py upload**. It may take few minutes for the ZTP process to finish.

7. To verify that VMs in the topology are running, you can open ssh session into node **vmm** and access serial console of the vmm

       ssh vmm
       vmm list
       vmm serial -t r1
       vmm serial -t gw
       vmm serial -t pe1

9. Now the lab is ready and can be used

