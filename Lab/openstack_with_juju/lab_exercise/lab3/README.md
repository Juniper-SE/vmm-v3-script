# Lab Exercise 3
In this lab exercise, the following will be configured
- create virtual network on the project
- Deploy VM on the project and test connectivity between virtual machine
- create  another virtual network
- Deploy VM on different virtual network
- Create logical router between virtual network and test connectivity between VMs which are connected to different virtual network
- Attach logical router to external network and test connectivity from VM to external network.


## Creating  virtual network and deploy Virtual machine
Creating virtual network and deployig virtual network can be done from openstack dashboard or contrail command dashboard.

For the first virtual network, it will be created through openstack dashboard

1. From the web browser, open openstack dashboard
2. Select project demo1
3. From the menu, select Project > Network > Networks, and click Create Network
4. Create a network with the following parameters
    - Network Name: Blue
    - Subnet:
        * subnet name: Blue
        * network address: 192.168.101.0/24
        * gateway: 192.168.101.1
5. Click Create to create the nework
6. From the menu, select Project > Compute > Instances, and click Launch Instances
7. Create VM instances with the following parameters
    - Instance Name:  VM-Blue
    - count: 2
    - Source: cirros
    - Flavor: m1.tiny
    - Networks: Blue
8. Click Launch instance to deploy the VMs
9. Verify that the VMs are deployed and running.
10. From the openstack dashboard, access the console of one of the VM, and test connectivity to the other VM
    - verify that the VM has been assigned with ip address accordingly
    - test connectivity to the other VM
11. On the next steps, virtual network and VM will be created through contrail command dashboard
12. From the web browser, open contrail command dashboard
13. on the top right page, select project demo1
14. From the menu, select Overlay > Virtual networks, and click Create.
15. Create virtual network with the following parameters
    - name: Red
    - subnets:
        CIDR : 192.168.102.0/24
16. Click Create to create virtual network
15. From the menu, select Workloads > Instances, and click Create
15. Create instances with the following parameters
    - Server type : Virtual Machine
    - Instance Name : VM-Red
    - Image: cirros
    - Select Flavor: m1.tiny
    - Allocated networks: Red
    - Availability Zone: Nova
    - Count: 2
16. Click Create to create the VMs
17. Verify that VMs are deployed and running. You may need to refresh the page.
18. Access console of the new VM, verify its ip address and connectivity to other vm connected to the same virtual network
19. Verify that VM-Red and VM-Blue are not able to communicate

## Creating logical router
Creating logical router can be done through openstack dashboard or contrail command dashboard.

In this exercise, we are going to use contrail command dashboard to create logical router

1. From the web browser, open contrail command dashboard
2. From the menu, select Overlay > Logical Routers, and click Create
3. Create logical router with the following parameters:
    - name: R1
    - Logical router type: SNAT Routing
    - Connected Network: Blue, Red
4. Click create to create the logical router
5. From VM-Blue, verify that it can reach VM-Red and vice versa
6. From either VM-Blue or VM-Red verify that the VMs are still not able to access external network (trying to ping 8.8.8.8 or 172.16.13.100)

## Connecting logical router to external network
1. Open ssh session into node gw, and verify that subnet 172.16.1.0/28 or its host routes is not yet advertised to this node.

        ip route show

2. open ssh session into node sdngw, and verify that subnet 172.16.1.0/24 or its host routes is not yet advertised to routing instance external1

        show route table external1.inet.0
3. From the web browser, open contrail command dashboard
4. From the menu, select Overlay > Logical Routers, select R1 and click Edit
5. Set External gateway to : External1
6. Click Save
7. On node sdngw, and verify that subnet 172.16.1.0/24 or its host routes has been received from contrail controller into routing table of routing instance external1

        show route table external1.inet.0

7. On node gw, verify a host route from subnet 172.16.1.0/28 or or its host routes has been be received from SDNGW

         ip route show

8. From any of the VM on the openstack cluster, test connectivity to external network (8.8.8.8 or 172.16.13.100)
9. Open ssh session into host 172.16.13.100 (ssh ubuntu@172.16.13.100), and verify that the source ip address of the ssh session is from subnet VN external (172.16.1.0/28)
10. Now connectivity from VM inside the openstack cluster and external network has been established


[Back to main page](../README.md)