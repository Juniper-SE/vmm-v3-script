#!/bin/bash
scp openstack_user_config.ovn.yaml root@ansible:/etc/openstack_deploy/openstack_user_config.yml
scp user_variables.yml root@ansible:/etc/openstack_deploy
scp nova.yml root@ansible:/etc/openstack_deploy/env.d/
scp neutron.yml root@ansible:/etc/openstack_deploy/env.d/
ssh root@ansible "mkdir -p /etc/openstack_deploy/group_vars"
scp network_hosts root@ansible:/etc/openstack_deploy/group_vars/
