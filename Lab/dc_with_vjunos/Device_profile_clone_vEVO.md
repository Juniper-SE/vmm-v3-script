# This document provides guideline on how to clone Device provile for Juniper vEVO (virtual Evo)

## Creating Device profile for vEVO
1. on Apstra Dashboard, select Device > Device Profiles
![clone_dp1](images/clone_dp1.png)
2. click Query All, and search for name PTX
![clone_dp2](images/clone_dp2.png)
3. Clone device profile **Juniper_PTX10001-36MR**
![clone_dp3](images/clone_dp3.png)
4. Set name of the cloned device profile to **Juniper vEVO** and set physical device to off
![clone_dp4](images/clone_dp4.png)
5. Click on Selector, and set the version to (20\\\.[34].*|2[1-3]\\\..*)-EVO$
![clone_dp5](images/clone_dp5.png)
6. Click on Ports, and delete the existing Panel, **Panel #1**
![clone_dp6](images/clone_dp6.png)
![clone_dp7](images/clone_dp7.png)
7. Add the new panel
![clone_dp8](images/clone_dp8.png)
8. set the number of port to 12 ports
![clone_dp9](images/clone_dp9.png)
9. click on port 1 to 12 to select port 1 to 12, 
![clone_dp10](images/clone_dp10.png)
10. on Display ID, click minus (-) sign to set the display ID to 0-11
![clone_dp11](images/clone_dp11.png)
![clone_dp11](images/clone_dp11a.png)
11. set Connector type to SFP+, and click add new transformation
![clone_dp11](images/clone_dp11b.png)
12. Set the template to **et-0/0/<display_id>**, and set interface speed and global speed to 1g, and click add transformation
![clone_dp12](images/clone_dp12.png)
![clone_dp13](images/clone_dp13.png)
13. Verify that each port is assigned with the correct port according to the following table

    port | template
    -|-
    0|et-0/0/0
    1|et-0/0/1
    2|et-0/0/2
    3|et-0/0/3
    4|et-0/0/4
    5|et-0/0/5
    6|et-0/0/6
    7|et-0/0/7
    8|et-0/0/8
    9|et-0/0/9
    10|et-0/0/10
    11|et-0/0/11

![clone_dp14](images/clone_dp14.png)
![clone_dp15](images/clone_dp15.png)
![clone_dp16](images/clone_dp16.png)

13. Click Clone to save the new Device profile
![clone_dp17](images/clone_dp17.png)
16. Now device profile for vEVO has been created
