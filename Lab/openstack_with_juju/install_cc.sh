#!/bin/bash
export CONTAINER_TAG=
docker run -dt \
        -v /home/ubuntu/command_servers.yml:/command_servers.yml \
        -e action=import_cluster \
        -e orchestrator=juju \
        -e delete_db=yes \
        -e juju_controller=172.16.11.100 \
        -e juju_controller_password=pass01 \
        -e juju_controller_user=ubuntu \
        -e juju_model=cn \
        --name contrail_command_deployer \
        hub.juniper.net/contrail/contrail-command-deployer:${CONTAINER_TAG}
