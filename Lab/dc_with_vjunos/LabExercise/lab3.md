# Lab 3, Site 1, Configuring Routing Zone, Virtual Network, and connectivity to External

## Objective
in this lab exercise, the following will be configured
- Routing Zone 
- Connecting routing zone to external network
- Virtual Network
- Connecting Server to Leaf Switch using untagged interface
- Connecting server to Leaf Switch using tagged interface
- Enabling DHCP services on Routing Zone/Virtual Network
- Connecting routing zone to external network using Stateful firewall


## Routing zone and Virtual Network for Site 1/DC1

|Routing Zone | Virtual Network | vlan-id | ipv4 subnet| ipv4 gateway| ipv6 subnet|ipv6 gateway|
|-|-|-|-|-|-|-|
|RZ1 | vn111| 111| 192.168.111.0/24| 192.168.111.254| fc00:dead:beef:a111::/64| fc00:dead:beef:a111::1|
|| vn112| 112| 192.168.112.0/24| 192.168.112.254| fc00:dead:beef:a112::/64| fc00:dead:beef:a112::1|
|RZ2| vn120| 120 | 192.168.120.0/24| 192.168.120.254| fc00:dead:beef:a120::/64| fc00:dead:beef:a120::1|
|| vn121| 121 | 192.168.121.0/24| 192.168.121.254| fc00:dead:beef:a121::/64| fc00:dead:beef:a121::1|
|| vn122| 122 | 192.168.122.0/24| 192.168.122.254| fc00:dead:beef:a122::/64| fc00:dead:beef:a122::1|
|RZ2| vn130| 130 | 192.168.130.0/24| 192.168.130.254| fc00:dead:beef:a130::/64| fc00:dead:beef:a130::1|
|| vn131| 131 | 192.168.131.0/24| 192.168.131.254| fc00:dead:beef:a131::/64| fc00:dead:beef:a131::1|
|| vn132| 133 | 192.168.132.0/24| 192.168.132.254| fc00:dead:beef:a132::/64| fc00:dead:beef:a132::1|

## Server connection to Leaf switches for Site 1/DC1

| server | port on server | Leaf Switch | port on leaf switch|
|-|-|-|-|
|svr1| eth0 | dc1leaf1| et-0/0/4|
||eth1| dc1leaf2|et-0/0/4|
|svr2| eth0 | dc1leaf1| et-0/0/5|
||eth1| dc1leaf2|et-0/0/5|
|kvm1| eth0 | dc1leaf1| et-0/0/6|
||eth1| dc1leaf2|et-0/0/6|
|svr3| eth0 | dc1leaf3| et-0/0/4|
||eth1| dc1leaf4|et-0/0/4|
|svr4| eth0 | dc1leaf3| et-0/0/5|
||eth1| dc1leaf4|et-0/0/5|
|kvm2| eth0 | dc1leaf3| et-0/0/6|
||eth1| dc1leaf4|et-0/0/6|
|svr5| eth0 | dc1leaf5| et-0/0/4|
||eth1| dc1leaf6|et-0/0/4|
|svr6| eth0 | dc1leaf5| et-0/0/5|
||eth1| dc1leaf6|et-0/0/5|
|kvm3| eth0 | dc1leaf5| et-0/0/6|
||eth1| dc1leaf6|et-0/0/6|
|kvm4| eth0 | dc1leaf7| et-0/0/7|
||eth1| dc1leaf8|et-0/0/7|

## Routing Zone and connectivity to external configuration
1. On Apstra dashboard, select blueprint **DC1**

2. on Blueprint **DC1**, select **Staged** > **Virtual** > **Routing Zones**, and click **Creating Routing Zone**

3. Create a routing zone with the following parameter
    VRF Name : RZ1
    
4. Set the EVPN L3 VNI using Default Pool

5. on Blueprint **DC1**, select **Staged** > **Physical**, and click on dc1leaf1.

6. On **dc1leaf1** add external generic, and create a new external system with the following parameter:
    - Name: ext
    - hostname: ext
    - representation of new device: None
    - system tag: ext
    - link: 
        * port et-0/0/4 of dc1leaf7
        * port et-0/0/4 of dc1leaf8

7. on Blueprint **DC1**, select **Staged** > **Connectivity Template** and click **Add template**

8. Create a new connectivity template with the following parameter
    - Title : to_ext_vlan1001
    - select pre-defined : BGP over L3 connectivity
    - Routing Zone : RZ1
    - interface type: tagged
    - vlan ID : 1001
    - ipv4/ipv6 addressing type: numbered
    - BGP Peering :
        * AFI : IPv4 and IPv6
        * IPv4/IPv6 addressing type: Addressed
    - Peer from/to: interface
    - Routing policy: default

9. on Blueprint **DC1**, select **Staged** > **Connectivity Template** and click **Assign**, and select port et-0/0/4 on dc1leaf7 and et-0/0/4 on dc1leaf8

10. on Blueprint **DC1**, select **Staged** > **Virtual** > **Routing Zone** > **RZ1**, scroll down to interfaces section, select all interfaces and click **Edit IP Address**, and set ip address according to the following table:

| Endpoint 1 | interface | ipv4 address | ipv6 address | Endpoint 2 | interface | ipv4 address | ipv6 address |
|--|--|--|--|--|--|--|--|
| dc1leaf7| et-0/0/4.1001| 10.1.101.0/31 | fc00:dead:beef:ff01::0/127 | ext | 10.1.101.1/31 |  fc00:dead:beef:ff01::1/127 |
| dc1leaf8| et-0/0/4.1001| 10.1.101.2/31 | fc00:dead:beef:ff01::2/127 | ext | 10.1.101.3/31 |  fc00:dead:beef:ff01::3/127 |

11. on Blueprint **DC1**, select **Staged** > **EXT** and click **Properties**, and change **ASN** to 65001

12. on Blueprint **DC1**, select **Staged** > **Virtual** > **Routing Zone**, and assign **Leaf loopback IP** and **Leaf loopback IP (IPv6)** to **Loopback_VRF_DC1**

13. Verify that none of the parameter on blueprint **DC1** are red flag

14. Commit configuration changes on blueprint **DC1**

15. Open SSH session into node **ext** and verify that BGP peer to dc1leaf7 and dc1leaf8 are up and running.


## Virtual Network configuration
1. on Blueprint **DC1**, select **Staged** > **Virtual** > **Virtual Network**, and click **Create Virtual Networks** 

2. Create a virtual network with the following parameter:
    - type: vxlan
    - name: vn111
    - routing zone: RZ1
    - vlan-id : 111
    - ipv4 connectivity: enabled
    - ipv4 subnet: 192.168.111.0/24
    - ipv4 gateway: 192.168.111.254
    - ipv6 connectivity: enabled
    - ipv6 subnet: fc00:dead:beef:a111::/64
    - ipv6 gateway: fc00:dead:beef:a111:1
    - Create connectivity template for tagged and unntaged
    - Assigned to :
        - rack_1_pair
        - rack_2_pair
3. Assign VNI  from default pool
4. Create another virtual network with the following parameter
    - type: vxlan
    - name: vn112
    - routing zone: RZ1
    - vlan-id : 112
    - ipv4 connectivity: enabled
    - ipv4 subnet: 192.168.112.0/24
    - ipv4 gateway: 192.168.112.254
    - ipv6 connectivity: enabled
    - ipv6 subnet: fc00:dead:beef:a112::/64
    - ipv6 gateway: fc00:dead:beef:a112:1
    - Create connectivity template for tagged and unntaged
    - Assigned to :
        - rack_1_pair
        - rack_2_pair
5. Assign VNI  from default pool
6. Commit configuration changes on blueprint **DC1**

## Assign port on Leaf to Virtual network (untagged)

1. on Blueprint **DC1**, select **Staged** > **Physical** > **dcleaf1**, and click **Add genering System** 

2. create a generic system with the following parameter
    - name: svr1
    - hostname: svr1
    - Apstra logical device: AOS-2x10-1
    - system tags: svr1
    - link on leaf switch and form LAG from these links
        - port et-0/0/4 on dc1leaf1
        - port et-0/0/4 on dc1leaf2

3. create another generic system with the following parameter
    - name: svr2
    - hostname: svr2
    - Apstra logical device: AOS-2x10-1
    - system tags: svr2
    - link on leaf switch and form LAG from these links
        - port et-0/0/5 on dc1leaf1
        - port et-0/0/5 on dc1leaf2

4. create another generic system with the following parameter
    - name: svr3
    - hostname: svr3
    - Apstra logical device: AOS-2x10-1
    - system tags: svr3
    - link on leaf switch and form LAG from these links
        - port et-0/0/4 on dc1leaf3
        - port et-0/0/4 on dc1leaf4

5. on Blueprint **DC1**, select **Staged** > **Connectivity template**  and click **assign** on  template **Untagged VxLAN vn111** and assigned ae interfaces of **svr1** and **svr3**

6. on Blueprint **DC1**, select **Staged** > **Connectivity template**  and click **assign** on  template **Untagged VxLAN vn112** and assigned ae interfaces of **svr2**

7. Commit configuration changes on blueprint **DC1**

8. configure ip address on svr1, svr2, and svr3 according to the following table

| server | interface LAG  | member of LAG | ipv4 address | ipv6 address|
|-|-|-|-|-|
|svr1 | bond0| eth0| 192.168.111.1/24| fc00:dead:beef:a111::1000:1/64|
||| eth1| gw: 92.168.111.254| |
|svr2 | bond0| eth0| 192.168.112.2/24| fc00:dead:beef:a112::1000:2/64|
||| eth1| gw: 92.168.112.254| |
|svr3 | bond0| eth0| 192.168.111.3/24| fc00:dead:beef:a111::1000:3/64|
||| eth1| gw: 92.168.111.254| |

9. Test connectivity between svr1 and svr3, svr1 and svr2, svr2 and svr3, from svr1/svr2/svr3, to external


## Create Virtual Networks and Assign port on Leaf to Virtual network (tagged)


1. on blueprint **DC1**, select **Staged** > **Physical** and click **dc1leaf1**, and add new generic systems with the following parameter:

| name/hostname | logical devices | port on leaf | mode | 
|----|----|----|---|
| kvm1| AOS-2x10-1 | ge-0/0/6 on dc1leaf1| LAG |
| | | ge-0/0/6 on dc1leaf2||
| kvm2| AOS-2x10-1 | ge-0/0/6 on dc1leaf3| LAG
| | | ge-0/0/6 on dc1leaf4||


2. Assign  
6. configure the following on node kvm1
    - ipv4 address of eth0 : 192.168.111.11/24 gateway 192.168.111.254
    - ipv6 address of eth0 : fc00:dead:beef:a111::1000:11
    - port eth1 and eth2 are bond using LACP and assigned to openvswitch.

7. Verify that node kvm1 is accessible

8. Create routing zone RZ2 with virtual network vn120, vn121, and vn122 (please refer to the table above)

9. Enable dhcp service on vn121 and vn122

10. Configure dhcp relay to 192.168.120.10 and fc00:dead:beef:a120::1000:10 on routing zone RZ2

11. Configure connectivity to external via node **ext** on vlan 1002

12. assign LAG port of dc1leaf1 ge-0/0/6 and dc1leaf2 ge-0/0/6 as tagged for vlan vn120, vn121, and vn122

13. Create one VM on kvm1, assign it to vlan vn120, and set ip address to 192.168.120.10/24(ipv4) and  fc00:dead:beef:a120::1000:10/64 (ipv6). Install dhcp server on this VM and create dhcp pool for subnet 192.168.121.0/24 and 192.168.122.0/24, and subnet fc00:dead:beef:a121::/64 and fc00:dead:beef:a122::/64






Go to the next [Lab exercise](lab4.md)

or 

Return to [Main Menu](README.md)
