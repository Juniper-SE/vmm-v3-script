# Lab exercise 2, Design
In this lab exercise, the following object will be created:
- logical devices
- interface map
- rack types
- template

## Creating Logical Devices
1. Open Apstra Web Dashboard
2. Select **Design**>**Logical Devices**
3. Click **Create logical Devices**
4. Enter the following parameters
    - Name: vEX_Spine
    - Number of port: 10
    - Create port group for all port with speed 1Gbps, connected to:
        - Superspine
        - leaf
        - generic

    ![lab2_pic1.png](images/lab2_pic1.png)
    ![lab2_pic2.png](images/lab2_pic2.png)

5. Click **Create logical Devices**
6. Enter the following parameters
    - Name: vEX_Leaf
    - Number of port: 10
    - Create port group with 2 port with speed 1Gbps, connected to:
        - Spine
    - Create port group with 8 port with speed 1Gbps, connected to:
        - Access
        - generic
    

    ![lab2_pic3.png](images/lab2_pic3.png)
    ![lab2_pic4.png](images/lab2_pic4.png)
    ![lab2_pic5.png](images/lab2_pic5.png)

5. Click **Create logical Devices**
6. Enter the following parameters
    - Name: vEX_Collapse
    - Number of port: 10
    - Create port group with 10 port with speed 1Gbps, connected to:
        - Spine
        - superspine
        - access
        - leaf
        - generic

    ![lab2_pic6.png](images/lab2_pic6.png)
    ![lab2_pic7.png](images/lab2_pic7.png)

7. Verify that three new logical devices has been created

    ![lab2_pic8.png](images/lab2_pic8.png)


## Creating Interface maps
1. Open Apstra Web Dashboard
2. Select **Design**>**Interface maps**
3. Click **Create Interface map**
4. Enter the following parameters
    - Name: vEX_Spine
    - Logical Device: vEX_Spine
    - Device profile: Juniper vEX
    - set port 0 to 9 to logical port groups

    ![lab2_pic9.png](images/lab2_pic9.png)
5. Select **Design**>**Interface maps**
6. Click **Create Interface map**
7. Enter the following parameters
    - Name: vEX_Leaf
    - Logical Device: vEX_Leaf
    - Device profile: Juniper vEX
    - set port 0 to 1 to logical port groups connected to spine
    - set port 2 to 9 to logical port groups connected to generic/access


    ![lab2_pic10.png](images/lab2_pic10.png)
    ![lab2_pic11.png](images/lab2_pic11.png)
8. Select **Design**>**Interface maps**
9. Click **Create Interface map**
10. Enter the following parameters
    - Name: vEX_Collapse
    - Logical Device: vEX_Collapse
    - Device profile: Juniper vEX
    - set port 0 to 9 to logical port groups

    ![lab2_pic10.png](images/lab2_pic12.png)


11. Verify that three interface maps has been created

    ![lab2_pic13.png](images/lab2_pic13.png)



## Creating Rack Types
1. Open Apstra Web Dashboard
2. Select **Design**>**Rack Types**
3. Click **Create Rack Type**
4. Enter the following parameters
    - Name: Rack_Type_1_ESI
    - Fabric Connectivity design: L3 Clos
    - Leaf Name: Leaf_ESI
    - Leaf Logical Device: vEX_Leaf
    - Redundancy protocol: ESI

    ![lab2_pic14.png](images/lab2_pic14.png)
    ![lab2_pic15.png](images/lab2_pic15.png)

5. Select **Design**>**Rack Types**
6. Click **Create Rack Type**
7. Enter the following parameters
    - Name: Rack_Type_2
    - Fabric Connectivity design: L3 Clos
    - Leaf Name: Leaf_Single
    - Leaf Logical Device: vEX_Leaf
    - Redundancy protocol: none

    ![lab2_pic16.png](images/lab2_pic16.png)
    ![lab2_pic17.png](images/lab2_pic17.png)
 

8. Select **Design**>**Rack Types**
9. Click **Create Rack Type**
10. Enter the following parameters
    - Name: Rack_Type_3
    - Fabric Connectivity design: L3 Collapsed
    - Leaf Name: Collapse
    - Leaf Logical Device: vEX_Collapse
    - Redundancy protocol: ESI

    ![lab2_pic18.png](images/lab2_pic18.png)
    ![lab2_pic19.png](images/lab2_pic19.png)

11. Verify that three Rack Types been created

    ![lab2_pic20.png](images/lab2_pic20.png)



## Creating Template
1. Open Apstra Web Dashboard
2. Select **Design**>**Templates**
3. Click **Create Template**
4. Enter the following parameters
    - Name: DC1
    - Type: Rack Based
    - Rack Type: Rack_Type_1_ESI, 3 unit
    - Spine logical devices: vEX_Spine
    - Spine count : 2

    ![lab2_pic21.png](images/lab2_pic21.png)
    ![lab2_pic22.png](images/lab2_pic22.png)


5. Select **Design**>**Templates**
6. Click **Create Template**
7. Enter the following parameters
    - Name: DC
    - Type: Collapsed
    - Rack Type: Rack_Type_3
    - mesh link speed: 1Gbps
  

    ![lab2_pic23.png](images/lab2_pic23.png)
    ![lab2_pic24.png](images/lab2_pic24.png)


8. Verify that two templates been created

    ![lab2_pic20.png](images/lab2_pic25.png)



[back to Lab Exercise](README.md)
