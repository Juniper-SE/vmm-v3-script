# lab exercise

## Create token for authentication
1. use script [create_token.py](API/create_token.py) to create token for authentication. it will create output file token.sh

        cd API
        source rd.sh
        ./create_token.py

## Creating organization and sites

1. use script [create_org.py](API/create_org.py) to create organization on routing director. before running this script, source script token.sh to load authentication token into environment variable and create environment variable ORG_NAME

        cd API
        source token.sh
        export ORG_NAME=vmm
        create_org.py

2.  use script [create_sites.py](API/create_sites.py) to create sites on routing director. This script requires input from file [sites.yaml](API/sites.yaml). Use script [get_sites_id.py](API/get_sites_id.py) to verify and create file sites_id.yaml, which will be used on the next step.

        source org.sh
        ./create_sites.py
        ./get_sites_id.py

## creating NIP (network implementation plan)
1. Use script [get_sernum.sh](./get_sernum.sh) to get serial number of devices on the network. It will create a file nodes_sernum.yaml, with the list of devices and its serial number

        ./get_sernum.sh

2. use script [create_NIP/create_nip.py]. This script requires two input files, sites_id.yaml and nodes_sernum.yaml, and the name of the NIP file

        cd create_NIP
        ./create_nip.py NIP1.json

3. Through the web dashboard, upload file NIP1.json into the Routing Director

## onboarding devices into routing director
1. use script [get_outbound_ssh_cmd.py](API/get_outbound_ssh_cmd.py) to get the ssh command for the network devices to be onboarded into routing director. it will generate output file onboarding.set.

        ./get_outbound_ssh_cmd.py

2. Edit file onboarding.set, you need to remove any line with **delete** command

3. use ansible playbook [upload_config.yaml](ansible/upload_config.yaml)

        ansible-playbook upload_config.yaml

4. login into web dashboard of routing director, and verify that onboarding process has started, and wait until the service status **ready for service** and **put into service**


