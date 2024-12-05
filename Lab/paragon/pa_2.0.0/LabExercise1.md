# Lab Exercise 1
## Configuring connectivity between Paragon Cluster and Network Devices

### IP address of Network Devices
node| loopback IP 
-|-
PE1|10.100.1.1
PE2|10.100.1.2
PE3|10.100.1.3
PE4|10.100.1.4
P1|10.100.1.11
P2|10.100.1.12
P3|10.100.1.13
P4|10.100.1.14
P5|10.100.1.15

1. Open ssh session to node1

        ssh node1

2. Try to reach loopback of the network devices. It should fail because routing is not properly configured yet
3. To fix it, enter the following configuration on node P5

        set routing-options static route 172.16.11.0/24 next-hop 172.16.14.0
        set policy-options policy-statement from_static term 1 from protocol static
        set policy-options policy-statement from_static term 1 then accept
        set protocols isis export from_static
        set protocols isis export from_static


4. Now from **node1**, it should be able to reach loopback for network devices

        ping 10.100.1.1
        ssh admin@10.100.1.1

5. Back to [main page](LabExercise.md)
