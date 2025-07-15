# do the following steps on Paragon 
1. Create organization
2. Create sites
3. create NIP (Network Implementation plan)
4. Onboard devices into Paragon Automation platform (brownfield onboarding)
5. Configure BGP-LS between Paragon Automation and network devices.


# using script to do above steps

1. Use script [create_site.py](config/paragon/NIP/create_site.py) to create organization and sites on paragon automation platform
2. Use script [get_sernum.sh](config/paragon/NIP/get_sernum.sh) to get serial number of network devices
3. USe cript [create_new_nip.py](config/paragon/NIP/create_new_nip.py) to create network implementation plan JSON file based on the template and the sites ID
4. Upload NIP file into paragon automation dashboard
5. Use script [ocssh.py](config/paragon/NIP/ocssh.py) to get the onboarding script from paragon automation platform
6. Use ansible playbook [update_router.yaml](config/paragon/NIP/update_router.yaml) to upload onboarding script into the network devices
7. Wait until all devices are onboarded, and change the onboard status from **Ready for Service** to **In service**
8. on Paragon Automation Dashboard, Observability > Topology, set Dynamic Topology (BGP-LS)
9. Verify that Link traffic dan delay statistic has been collected by Paragon (you may have to wait for a few minutes). If link traffic is empty, go to one of the paragon node, and restart pod pf-telemetry 
