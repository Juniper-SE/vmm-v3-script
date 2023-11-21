# Lab Exercise 4
In this lab exercise, the following will be configured
- Floating ip pools
- Floating ip and assign it to the virtual machine
- Security group to allow incoming traffic

## Creating Floating IP pools
1. From the web browser, open contrail command dashboard
2. From the top right of the dashboard, select project admin
2. From the menu, select Overlay > Floating IPs > Floating IP Pools, and click create
3. Create a floating ip pools with the following parameter:
    - name : External1 FIP
    - network: External1
4. Click Create.

## Create Floating IP and assign it to the VM
1. From contrail command dashboard, Select project demo1
2. From the menu select Overlay > Floating IPs > All Floating IPs, and click create
3. Select Floating IP Pools : External1 FIP, and number of IP Addresses: 1
4. Click Create to create one floating ip
5. From the menu, select Overlays > Virtual Ports, and select the port of the VM that the floating ip will be assigned to, for example ip address 192.168.101.3, and click edit
6. on the floating IPs field, assign the floating ip that was created on step 1-4, and click save
7. Now the VM has been assign with floating ip.
8. open ssh session into node sdngw, and verify that the floating ip has been advertised by contrail controller to SDN gateway into routing instance external1

        show route table external1.inet.0
9. Open ssh session into node gw, and verify that the floating ip has been advertised by SDNGW to node GW

        ip route show

10. Open ssh session into node ext1 (ip address 172.16.13.100), and try to ping or open ssh session into the floating ip address. It will fail because by default on openstack cluster, VMs are assigned with default SG (Security group) that allow only traffic from internal.

## Create a new security group and assign it to the Virtual machine.
1. From contrail command dashboard, Select project demo1
2. From the menu, select Overlay > Security Group and click Create
3. Create a new security group with the following parameters
    - Name: Allow1
    - Add two new Security group rules with the following parameters
        * Direction: ingress
        * Ether type: ipv4
        * type: CIDR
        * address: 0.0.0.0/0
        * protocol: tcp
        * port: 22-22
        and 
        * Direction: ingress
        * Ether type: ipv4
        * type: CIDR
        * address: 0.0.0.0/0
        * protocol: ICMP
4. Click Create to create the security group
5. From the menu, select Overlay > Virtual Ports, and select the virtual port that has been assigned with floating ip and click edit.
6. On the security group field, add the new security group Allow1. Put SG Allow1 before SG default
7. Click Save
8. From node ext1, verify that it can ping and open ssh session into  the floating ip 


## SSH into VM from external network using ssh certificate
1. on node ext1, create a new ssh key

        ssh ext1
        ssh-keygen -t rsa
        cat .ssh/id_rsa.pub

2. Copy the public key of the ssh key
3. On the openstack dashboard, select project demo1
4. From the menu, select Project > Compute > Key Pairs, and click import public key.
5. Set the key name for example ext1, key type to SSH key, and paste the public key
6. Click import key
7. Select menu Project > Compute > Instances and select Launch Instances.
8. Create a new VM with the following parameter
    - instance name: debianVM
    - count: 1
    - source: debian
    - flavor: m1.small
    - networks: Blue 
    - security group: Allow1, default
    - key pair: ext1
9. Click Launch Instance to deploy the VM
10. From the menu, select Project > Network > Floating IPs, and click Allocate IP To Project
11. Click Allocate IP
12. From the menu, Project > Network > Floating IPs, select the new floating ip, and click Associate
13. For the field Port to be associated, select port debianVM (the one that was create on step 7-9), and click associate.
14. open ssh session into node sdngw, and verify that the floating ip has been advertised by contrail controller to SDN gateway into routing instance external1

        show route table external1.inet.0
15. Open ssh session into node gw, and verify that the floating ip has been advertised by SDNGW to node GW

        ip route show
16. From node ext1, try to ping the new floating ip address

        ping 172.16.1.5  # for example 172.16.1.5 is the new floating ip 

17. From node ext1, try to open ssh into the new floating ip address

        ssh debian@172.16.1.5   # debian is the default user of debian VM

[Back to main page](../README.md)