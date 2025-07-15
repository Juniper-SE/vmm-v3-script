sudo yum -y  remove python-requests
docker run -td --net host -v /home/centos/command_servers.yml:/command_servers.yml --privileged --name contrail_command_deployer hub.juniper.net/contrail/contrail-command-deployer:2011.L2.372
