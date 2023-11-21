docker run -dt \
  --name contrail_command_deployer \
  -v /home/ubuntu/command_servers.yml:/command_servers.yml \
  -e action=import_cluster \
  -e orchestrator=juju \
  -e delete_db=yes \
  -e juju_controller=172.16.11.100 \
  -e juju_controller_password=pass01 \
  -e juju_controller_user=ubuntu \
  -e juju_model=cn \
  hub.juniper.net/contrail/contrail-command-deployer:21.3.1.98
