# This document provides guideline on how to use Routing Director lab

## Preparation for the lab.

In this step, we are going to update DNS server inside the routing director lab, to include vJunosRouter nodes.

1. open ssh session to node **gw** of lab **routing_director**, verify that vJunosRouter nodes are not included yet in the DNS database

       ssh ubuntu@172.16.11.254 -i ~/.ssh/rd 
       ubuntu@gwrd:~$ cat /etc/coredns/vmmlab.com.db
       $ORIGIN vmmlab.com.
       @    IN       SOA    vmmlab.com. mir.vmmlab.com 2502011720 7200 3600 1209600 3600
       desktop1 IN A 172.16.11.50
       node1 IN A 172.16.11.11
       node2 IN A 172.16.11.12
       node3 IN A 172.16.11.13
       node4 IN A 172.16.11.14

2. Add vJunosRouter nodes into the DNS database

       cat << EOF | sudo tee -a /etc/coredns/vmmlab.com.db
       pe1  IN  A  10.100.255.1
       pe2  IN  A  10.100.255.2
       pe3  IN  A  10.100.255.3
       pe4  IN  A  10.100.255.4
       pe5  IN  A  10.100.255.5
       p1  IN  A  10.100.255.11
       p2  IN  A  10.100.255.12
       p3  IN  A  10.100.255.13
       p4  IN  A  10.100.255.14
       p5  IN  A  10.100.255.15
       crpd  IN  A  10.100.255.10
       EOF
       sudo systemctl restart coredns
       ping pe1
       ping p1
       ping pe5

3. open ssh session into one of the routing director node, and test connectivity to vJunosRouter nodes

       ssh root@172.16.11.11
       exit
       ping p1
       ping pe1
       ssh admin@pe1

## Create Network Implementation Plan (NIP) on Routing Director

1. Access web dashboard of Routing director, http://172.16.12.1

2. if Organization is not yet created, create one, for example create an organization called **vmm** or **lab**

3. Navigate to **Inventory** > **Sites**, and click **+** to create a site. Create 10 sites for all the vJunosRouter nodes.

4. Navigate to **Inventory** > **Network Implementation Plan**, and click **+** to create a new NIP

5. Click **next** to add device, and click **+**. Set the device name, site, serial number, vendor, and model.

6. To get the serial number of the devices, use this shell script [get_sernum.sh](./get_sernum.sh) or use ansible-playbook [get_sernum.yaml](ansible/get_sernum.yaml) 

7. Navigate to **Inventory** > **Network Inventory**, and click **add device**, copy the cli command

8. Open ssh session into node **pe1**, and paste the cli command into the configuration mode.

9. Repeat step 7 for all the vJunosRouter nodes (PE2, PE3, PE4, PE5, P1, P2, P3, P4, and P5)

10. Or you can upload the configuration using ansible playbook [upload_config.yaml](ansible/upload_config.yaml). Before using the ansible script, save the cli command from step 7 into file [onboarding.set](ansible/onboarding.set)

        cd ~/git/vmm-v3-script/Lab/routing_director/lab_exercise/ansible
        cat << EOF | tee onboarding.set
        ...
        EOF
        ansible-playbook upload_config.yaml

11. Routing Director will start the onboarding process.
12. Navigate to **Inventory** > **Network Inventory**, and wait until all devices status become **Ready for Service**
13. Navigate to **Inventory** > **Onboarding Dashboar**, select all devices and click **Put into Service**
14. 
14. Now you can start playing around with Routing Director

