# This document provides guideline on how to use Routing Director lab


## Create Network Implementation Plan (NIP), onboarding device on Routing Director, using GUI

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


## Create Network Implementation Plan (NIP), onboarding device on Routing Director, using GUI

please follow this [document](./lab_exercise.md) to use API to create NIP 
