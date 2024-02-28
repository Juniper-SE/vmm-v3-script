# Lab 2, Site 1 Datacenter Fabric Configuration

## Objective
- Configure resources (ASN pools and IP/IPv6 Pools)
- configure Logical devices
- Configure interface map
- configure Rack types
- configure Templates
- configure configlet
- Creating and deploying Blueprint

## Resources for the lab exercise

### ASN Pools for Site 1

| Name | ASN |
|-|-|
|ASN_Spine_DC1| 4200001001 - 4200001009|
|ASN_Leaf_DC1| 4200001011 - 4200001019|

### IP pools for Site 1
| Name| IP pool|
|-|-|
|Fabric_Link_DC1| 10.101.0.0/24|
|Loopback_Spine_DC1|10.101.1.0/24|
|Loopback_Leaf_DC1|10.101.2.0/24|
|Loopback_VRF_DC1| 10.101.3.0/24|

### IPv6 pools for Site 1
| Name| IP pool|
|-|-|
|Loopback_Spine_DC1|fc00:dead:beef:1011::/64|
|Loopback_Leaf_DC1|fc00:dead:beef:1012::/64|
|Loopback_VRF_DC1| fc00:dead:beef:1013::/64|

## Configure Resources (ASN Pools and IP/IPv6 Pools)


1. On Apstra dashboard, click **Resources** > **ASN Pools**, and click **Create ASN Pool**

2. Create ASN pools based on the table above

![asn_pools](images/asn_pools.jpg)

3. On Apstra dashboard, click **Resources** > **IP Pools** and click **Create IP Pools**

4. Create IP Pools based on the table above

![ip_pools](images/ip_pools.jpg)

5. On Apstra dashboard, click **Resources** > **IPv6 Pools** and click **Create IPv6 Pools**

6. Create IPv6 Pools based on the table above

![ip_pools](images/ipv6_pools.jpg)

## Configure logical devices 
1. On Apstra dashboard, click **Design** > **Logical Devices**, and click **Create Logical Device**

2. Create a logical device with the following parameter
    - name: AOS-10x10
    - number of port: 10
    - Speed: 10Gbps
    - Port group with 10 Port, and connected to: 
        * spine
        * superspine
        * leaf
        * access
        * Peer
        * Unused
        * Generic

    ![logical_devices](images/logical_device1.jpg)
    ![logical_devices](images/logical_device2.jpg)
    ![logical_devices](images/logical_device3.jpg)

## Configure Interface Maps
1. On Apstra dashboard, click **Design** > **Interface Maps**, and click **Create Interface Map**

2. Create an interface map with the following parameters:
    - name : vJunos_10_Ports
    - Logical device: AOS-10X10
    - Device Profile: vJunos-switch 10 Ports
    - Assign all interface

    ![Interface_map](images/interface_map1.jpg)

3. Create another interface map with the following parameters:
    - name : vJunosEVO_10_Ports
    - Logical device: AOS-10X10
    - Device Profile: vJunosEvolved 10 Ports
    - Assign all interface

    ![Interface_map](images/interface_map2.jpg)

    ![Interface_map](images/interface_map3.jpg)


## Configure Rack Type

1. On Apstra dashboard, click **Design** > **Rack Types**, and click **Create In Builder**

2. Create a rack type with the following parameter
    - Name: Rack_Type_1
    - Fabric connectivity design: L3 Clos
    - Leaf Name: Leaf
    - Leal Logical Device: AOS-10X10
    - Redundancy Protocol: ESI

3. Click **Create** to create the new rack type

    ![rack_type](images/rack_type1.jpg)
    ![rack_type](images/rack_type2.jpg)

## Configure Template
A template with 2 Spine switches and 6 Leaf switches will be create in this exercise

1. On Apstra dashboard, click **Design** > **Templates**, and click **Create Templates**

2. Create a Template with the following parameter
    - Name: Spine-Leaf
    - Type: Rack Based
    - ASN Allocation Scheme: Unique
    - Overlay control protocl: MP-EBGP EVPN
    - Rack type: Rack_Type_1
    - Number of rack: 3
    - Spine Logical DevicesL: AOS-10X10
    - Spine Count: 2
    - Leal Logical Device: AOS-10X10
    - Redundancy Protocol: ESI

3. Click **Create** to create the new rack type

    ![template](images/template1.jpg)
    ![template](images/template2.jpg)
    ![template](images/template3.jpg)


## Configuring Blueprint

1. On Apstra dashboard, click **Blueprints**, and click **Create Blueprint**

2. Create a blueprint with the following parameter
    - Name: DC1
    - Reference Design: Datacenter
    - Template: DC1

3. Click **Create** to create the blueprint

    ![blueprint](images/blueprint1.jpg)
    ![blueprint](images/blueprint2.jpg)

4. Click blueprint **DC1** to modify blueprint configuration

5. Click **Stage** > **Fabric Settings** > **Fabric policy** and click **Modify Settings**, and enable **IPv6 Applications**, and click **Save Changes**

    ![blueprint](images/lab2_bp_enable_ipv6_1.jpg)
    ![blueprint](images/lab2_bp_enable_ipv6_2.jpg)

6. Click **Stage** > **Physical** > **Resources**

    ![blueprint](images/lab2_bp_resources1.jpg)

7. Assign the resources, such as ASN for spine and Leaf, IP Loopback and IPv6 Loopback for Spine and Leaf, Link's IP Spine <> Leaf. Use the resources (ASN, IP Pools, IPv6 Pools that was created on the previous lab)

    ![blueprint](images/lab2_bp_resources2.jpg)

8. Click **Stage** > **Physical** > **Device Profiles**

    ![blueprint](images/lab2_bp_dp_1.jpg)
7. Assign interface map **vJunosEVO_10_Ports** to all devices

    ![blueprint](images/lab2_bp_dp_2.jpg)
    ![blueprint](images/lab2_bp_dp_3.jpg)

8. change the name of the devices based on the following table

| old name| new name|
|---|----|
|spine1|dc1spine1|
|spine2|dc1spine2|
|rack_type_1_001_leaf1|dc1leaf1|
|rack_type_1_001_leaf2|dc1leaf2|
|rack_type_1_002_leaf1|dc1leaf3|
|rack_type_1_002_leaf2|dc1leaf4|
|rack_type_1_003_leaf1|dc1leaf5|
|rack_type_1_003_leaf2|dc1leaf6|


![blueprint](images/lab2_bp_change_name_1.jpg)
![blueprint](images/lab2_bp_change_name_2.jpg)

9. Change the rack name based on the following table

|old name | new name|
|-|-|
|rack_type_1_001| rack_1|
|rack_type_1_002| rack_2|
|rack_type_1_003| rack_4|

![blueprint](images/lab2_bp_change_name_3.jpg)
![blueprint](images/lab2_bp_change_name_4.jpg)

10. Change the pair name based on the following table

| rack | old pair name | new pair name|
|--|---|---|
|rack_1| rack_type_1_001_leaf_pair1 | rack_1_pair|
|rack_2| rack_type_1_002_leaf_pair1 | rack_2_pair|
|rack_4| rack_type_1_003_leaf_pair1 | rack_4_pair|

15.  Click **Stage** > **Physical** > **Devicess** and click **Assign System ID**

![blueprint](images/lab2_bp_assign_systemid_1.jpg)
![blueprint](images/lab2_bp_assign_systemid_2.jpg)

16. Assign the system ID according to the following table, and set the deploy mode to **deploy** for all devices

| Name | System ID|
|-|-|
|dc1spine1| 172.16.11.101|
|dc1spine2| 172.16.11.101|
|dc1leaf1| 172.16.11.111|
|dc1leaf2| 172.16.11.112|
|dc1leaf3| 172.16.11.113|
|dc1leaf4| 172.16.11.114|
|dc1leaf7| 172.16.11.115|
|dc1leaf8| 172.16.11.116|


![blueprint](images/lab2_bp_assign_systemid_3.jpg)
17. Click **Update Assignment** to update system ID assignment

18. Click tab **Uncommitted**, verify that there is no Red color on Logical diff or Full nodes diff, and click **Commit** to deploy the blueprint. 

![blueprint](images/lab2_bp_deploy_1.jpg)

![blueprint](images/lab2_bp_deploy_2.jpg)

![blueprint](images/lab2_bp_deploy_3.jpg)

19. Open ssh session into one of the devices to verify that blueprint has been properly deployed

![blueprint](images/lab2_bp_deploy_4.jpg)

![blueprint](images/lab2_bp_deploy_5.jpg)

Go to the next [Lab exercise](lab3.md)

or 

Return to [Main Menu](README.md)

