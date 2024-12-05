# How to use Juniper VMM

release 0.8
## Overview
This script is used to create configuration files, which will be used to create and run VMs (Virtual Machines) on Juniper's VMM infastructure.
The scripts has been modified to work with VMM 3.0 

## update on the script
new features has been added into the scripts :

~~- allow access into the VMM lab using the jump host. Please edit the lab.yaml to specify which VMM lab that you want to use and the jump host to access that lab.~~
- vpn is no longer required, everything is handled by zscaler connect
- jump host is no longer required
- using jinja2 template to create configuration for junos devices. Currently it support configuration for the following :
    * address family : inet, inet6  (work in progress), iso, mpls
    * protocols : isis, mpls, rsvp, ldp, pcep, bgp-ls
- topology of point-to-point connection between junos devices can be generated automatically, for both bridge assignment and address (ipv4/ipv6) allocation
- On VMM 3.0, configuration of PC's VM is no longer written to the disk image when the VM was started for the first time, so on this script, the configuration of the PC is pushed using ssh, therefore PC VMs must be assigned with IP address
- the IP address assignment to the PC VMs is done using dhcp with node GW as the dhcp server
- create wireguard configuration for direct connection into the nodes in the Lab. 


## The supported VMs :
- vMX
- vSRX
- vEVO/vPTX
- Apstra fabric controller
- PC with ubuntu OS 
- PC with centos OS
- bridge using Alpine linux to provide Delay or packet loss between Nodes

## Requirement
This script requires the following :
- Python3 (this script requires Python3)
- passlib library (to install use `pip3 install passlib`)
- paramiko library (to install use `pip3 install paramiko`)
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
- the ssh key to access jumphost, vmm server and the VMs inside the topology. 
- JNPR Lab Domain password (to access vmm server)
  - if you don't to hardcode your VMM password into file lab.yaml, your can set environment variable VMMPASSWORD with your JNPRLAB domain password

        export VMMPASSWORD="what ever is your password"

- the script assume the ssh key files are located inside directory ~/.ssh 
  - the private key to be ~/.ssh/<ssh_key_name> 
  - public key to be ~/.ssh/<ssh_key_name>.pub
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
- argument `init_junos`: to send configuration to vEX and/or vPTX
- argument `create_gw_config`: to create wireguard configuration

## Caution

- when the script is used to start the topology, any existing running topology will be stopped and unbound. Please backup the existing topology if needed.
- on one pod location, only one VMM topology can run. If you need to run multiple topology, then you need to run those topology on different VMM pod.

## Accessing the VMM Lab

Because of the network segmentation policy, VMM servers are not accessible directly from Juniper's intranet, jumphost is required to access the VMM server.

The following table are the available jump host for each location. There are multiple jump hosts and each jump host has maximumm number of users that can login.

![table1](jh_vmm_server.png)

To access jump host and VMM server, use your active directory username/password.

Unix password is no longer required.

You can also use ssh key to have passwordless access into the jump host and vmm server, although it may not work for all jump hosts, since not all jump hosts provide the home directory for your user-ID. The script will assume that ssh key <ssh_key_name> is used for accessing jumphost and vmm server.

## Step by Step guide on how to use the script

1. Create configuration file for the lab **lab.yaml**. You can refer to the sample under directory lab.
2. Run the script with argument `upload`, to upload the configuration files into VMM server. The script will ctreate the configurations under directory `./tmp`. Files inside these directory will be uploaded into VMM server.

        ../../vmm.py upload

3. Run the script with argument `start`, to start the topology on VMM. Remember any active topology will be stop and destroyed. Remember to backup the configuration of any existing running topology

        ../../vmm.py start


4. Verify that node GW is up and running, by initiating ssh session into it. The username to access node GW is **pass01**

        ssh gw

5. Run the script with argument `set_gw`, to configure other interfaces of node gw (interface em1, em2, etc), upload ssh key and dhcp server configuration. Node **GW** will be acting as DHCP server for on ubuntu/centos VM in the topology

        ../../vmm.py set_gw


6. Run the script with argument `set_host`, to configure Linux VM, such has hostname, change interface configuration from dhcp to static, and upload ssh key.

        ../../vmm.py set_host

6. If there are vEX (vJunos) and/or vPTX/vEVO in the topology, then run the script with argument `init_junos`,  vEX and vPTX.

        ../../vmm.py init_junos

9. Now the lab is ready and can be used

