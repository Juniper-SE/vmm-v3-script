# Change default password and upload the license
1. Login into Paragon dashboard using user **admin** and change the password from default to new password
2. Login into Paragon dashboard using new password
3. On paragon dashboard, select **Administration** > **License Management**, and add the licenses into Paragon platform
4. Logout and login again to verify that license has been activated 

# Initial setup for paragon automation

1. On Paragon node **node1** or **node2** or **node3**,  test connectivity to loopback of network devices (10.100.1.1, 10.100.1.2, 10.100.2.5, 10.100.2.6, 10.100.3.10, 10.100.3.11)

2. On node **r1**, verify that BGP peer with **crpd** on Paragon automation is up and running
    ![p4_bgp](images/p4_bgp.jpg)

3. On Paragon Automation dashboard, click **Network** > **Topology** and verify that network topology are discovered

    ![network_topology](images/network_topology.jpg)

4. On Paragon Dashboard, click **Configuration** > **Device**, click **Add**, select **Add targets from topology to this list**, select all devices to be added, and set device credentials to admin/pass01, and click **OK**. Wait until job is done.

    ![add_devices1](images/add_devices1.png)
    ![add_devices2](images/add_devices2.png)
    ![add_devices3](images/add_devices3.png)
    ![add_devices4](images/add_devices4.png)
    ![add_devices5](images/add_devices5.png)
    ![add_devices6](images/add_devices6.png)

5. On Paragon Dashboard, click **Configuration** > **Device Groups**. Select group **controller** and click **edit**
   and add all device into group **controller**. Click Save and Deploy  

    ![dg1](images/dg1.png)
    ![dg2](images/dg2.png)

6. On Paragon Dashboard, click **Configuration** > **Device**, select all devices, and click **Edit**.
    ![editdevices1](images/editdevices1.png)
7. Do not change the parameter here. just leave it as it is.
    ![editdevices2](images/editdevices2.png)
8. Set SNMP community, PCEP Version to RFC compliant,  and enabled Netconf for all devices. Click **OK** to save
    ![editdevices3](images/editdevices3.png)

11. Go to **Network** > **Topology** and verify it on the table
    ![verify1](images/verify1.png)

12. Go to **Administration** > **Task Scheduler** and click **Add**
    ![taskscheduler1](images/taskscheduler1.png)

13. Create a new task, with task type : Device collection
    ![taskscheduler2](images/taskscheduler2.png)

14. Click Next, for collection options, Select All, and click **Next**
    ![taskscheduler3](images/taskscheduler3.png)

15. Click Next, for Recurrence options, set repeat every 15 minutes or 1 hour, and click **submit**. Wait until the task is finish
    ![taskscheduler4](images/taskscheduler4.png)
    ![taskscheduler5](images/taskscheduler5.png)

16. To verify, go to **Network** > **Topology**, and click **link**. Interface informations, such as ge-0/0/0, are available through dashboard
    ![verify2](images/verify2.png)

17. Select one of the link, then from menu **View**, select to display **Interface traffic** or **Interface Delay**
    ![verify3](images/verify3.png)
    ![verify4](images/verify4.png)
    ![verify5](images/verify5.png)

18. To Enable LSP Delay calculation, do the following steps  (the following steps is not required on Paragon version 21.2)
19. From your workstation, open SSH session into node **node0**

        ssh node0

20. On node **node0**, run this command to get the name of pod CMGD and run cli command on container ns-cmgd

        kubectl get pods -A | grep cmgd

21. Run the following command to access CLI on container ns-cmgd

        kubectl exec -n northstar -it <pod_name> -c ns-cmgd -- cli

        kubectl -n northstar exec -it `kubectl -n northstar get pods | grep cmgd | tr -s " " | cut -f 1 -d " "` -c ns-cmgd cli

22. Run the following command on the CLI

        edit
        set northstar path-computation-server lsp-latency-interval 60s
        set northstar path-computation-server analytics reroute-minimum-interval 3m
        commit

![cmgd](images/cmgd.png)

23. Now Delay will be calculated for the LSP and reroute LSP dynamically

24. on Paragon dashbard, from the left pane, click **Configuration** > **Data Ingest** > **Setting**, select **native gpb**, set the port (it must patch with the port configuration of the junos devices, on streaming profile configuration ).
25. Click **save and deploy**

![ingest](images/ingest.png)


26. Now you can explore different features of Paragon Automation. 
27. you can explore the lab exercise [document](lab_exercise.md) that I've created.

