# deploying openstack using charm

## configure juju controller

1. login into node client, and install juju client

       sudo snap install juju

       sudo snap install juju --channel 3.1
       sudo snap install vault

2. create/bootstrap juju controller on node juju (172.16.11.101)

       juju bootstrap manual/ubuntu@172.16.11.101 vmm
       juju add-model --config default-series=jammy openstack

3. Add host (node0, node1, node2, node3) into the controller

       for i in {0..3}; do echo "add 172.16.11${i} into juju"; juju add-machine ssh:ubuntu@172.16.11.11${i}; done

4. Deploy LXD on node0, node1, node2, node3

       juju deploy -n 4 --to 0,1,2,3 --config lxd-init-network=false  lxd

## deploy LXC container on compute nodes (node0, node1, node2, node3)
1. open ssh session to node0

       ssh node0

2. list the available ubuntu images from the remote server, and get ID of the latest image for ubuntu 22.04 (jammy)

       lxc image list ubuntu: | grep 22.04 | grep CONTAINER | grep amd64 

3. download the image into local node0

       lxc image copy ubuntu:<image_id> local: --alias ubuntu22.04
       
       lxc image copy ubuntu:fd08b20350dd local: --alias ubuntu22.04
       

4. download the same image into node1, node2, node3

       ssh node1
       lxc image copy ubuntu:fd08b20350dd local: --alias ubuntu22.04
       lxc image ls

5. upload scripts in directory [script_to_create_lxc_container](./script_to_create_lxc_container). use script [upload_file.sh](./script_to_create_lxc_container/upload_file.sh) to upload scripts into node client, node0, node1, node2, node3

       cd ./script_to_create_lxc_container
       ./upload_file.sh

6. open ssh into node0, and run the scripts

       ./create_container_node0.sh

       # wait until all container has ip address
       lxc ls
       ./set_ip_container_node0.sh
       lxc ls

7. repeat step 6 on node1, node2, and node3
8. on node client, run script [add_machine](./script_to_create_lxc_container/add_machine.sh) to add the LXC containers into juju

       ssh client
       juju status
       ./add_machine.sh 
       
9. verify that there are 20 machines has been added into juju manually

       juju status


## deploy openstack
0. Open ssh session into client and do the following steps, or you can upload script from [directory ./deploy_openstack_script](./deploy_openstack_script/) into node client, and run it one by one (there are 17 scripts )

       cd deploy_openstack_script
       scp * client:~/
       ssh client
       ./step_1_deploy.sh
       ./step_2_deploy_nova_compute.sh 
       ...
       

1. Deploy Ceph OSD

       cat << EOF | tee ceph-osd.yaml
       ceph-osd:
         osd-devices: /dev/sdb /dev/sdc
       EOF

       juju deploy -n 4 --to 0,1,2,3 --channel reef/stable --config ceph-osd.yaml ceph-osd

2. Deploy Nova compute

       cat << EOF | tee nova-compute.yaml
       nova-compute:
         config-flags: default_ephemeral_format=ext4
         enable-live-migration: true
         enable-resize: true
         migration-auth-type: ssh
         virt-type: kvm
       EOF

       juju deploy -n 4 --to 0,1,2,3 --channel 2023.2/stable --config nova-compute.yaml nova-compute

3. Deploy MySQL InnoDB

       # juju deploy -n 3 --to lxd:0,lxd:1,lxd:2 --channel 8.0/stable mysql-innodb-cluster
       juju deploy -n 3 --to 4,5,6 --channel 8.0/stable mysql-innodb-cluster

4. Deploy vault

       # juju deploy --to lxd:3 --channel 1.8/stable vault
       juju deploy --to 7 --channel 1.8/stable vault
       juju deploy --channel 8.0/stable mysql-router vault-mysql-router
       juju integrate vault-mysql-router:db-router mysql-innodb-cluster:db-router
       juju integrate vault-mysql-router:shared-db vault:shared-db
            
5. Initialize and unseal vault

       export VAULT_ADDR="http://172.16.11.154:8200"
       vault operator init -key-shares=5 -key-threshold=3

       vault operator unseal <key1>
       vault operator unseal <key2>
       vault operator unseal <key3>

       export VAULT_TOKEN=<initial_token>
       vault token create -ttl=10m
       juju run  vault/leader authorize-charm token=<token>
       juju run vault/leader generate-root-ca

       juju integrate mysql-innodb-cluster:certificates vault:certificates

6. Deploy neutron

       cat << EOF | tee neutron.yaml
       ovn-chassis:
          bridge-interface-mappings: br0:eth0
          ovn-bridge-mappings: physnet1:br0
       neutron-api:
          neutron-security-groups: true
          flat-network-providers: physnet1
       EOF


       # juju deploy -n 3 --to lxd:0,lxd:1,lxd:2 --channel 23.09/stable ovn-central
       juju deploy -n 3 --to 8,9,10 --channel 23.09/stable ovn-central

       # juju deploy --to lxd:1 --channel 2023.2/stable --config neutron.yaml neutron-api
       juju deploy --to 11 --channel 2023.2/stable --config neutron.yaml neutron-api

       juju deploy --channel 2023.2/stable neutron-api-plugin-ovn
       juju deploy --channel 23.09/stable --config neutron.yaml ovn-chassis
       # juju deploy --channel 2023.2/stable neutron-dynamic-routing
       juju integrate neutron-api-plugin-ovn:neutron-plugin neutron-api:neutron-plugin-api-subordinate
       juju integrate neutron-api-plugin-ovn:ovsdb-cms ovn-central:ovsdb-cms
       juju integrate ovn-chassis:ovsdb ovn-central:ovsdb
       juju integrate ovn-chassis:nova-compute nova-compute:neutron-plugin
       juju integrate neutron-api:certificates vault:certificates
       juju integrate neutron-api-plugin-ovn:certificates vault:certificates
       juju integrate ovn-central:certificates vault:certificates
       juju integrate ovn-chassis:certificates vault:certificates



       juju deploy --channel 8.0/stable mysql-router neutron-api-mysql-router
       juju integrate neutron-api-mysql-router:db-router mysql-innodb-cluster:db-router
       juju integrate neutron-api-mysql-router:shared-db neutron-api:shared-db

7. deploy keystone

       # juju deploy --to lxd:0 --channel 2023.2/stable keystone

       juju deploy --to 12  --channel 2023.2/stable keystone

       juju deploy --channel 8.0/stable mysql-router keystone-mysql-router
       juju integrate keystone-mysql-router:db-router mysql-innodb-cluster:db-router
       juju integrate keystone-mysql-router:shared-db keystone:shared-db

       juju integrate keystone:identity-service neutron-api:identity-service
       juju integrate keystone:certificates vault:certificates

8. deploy rabbitMQ

       # juju deploy --to lxd:2 --channel 3.9/stable rabbitmq-server
       juju deploy --to 13 --channel 3.9/stable rabbitmq-server
       juju integrate rabbitmq-server:amqp neutron-api:amqp
       juju integrate rabbitmq-server:amqp nova-compute:amqp

9. Deploy nova cloud controller

       cat << EOF | tee ncc.yaml 
       nova-cloud-controller:
          network-manager: Neutron
       EOF

       # juju deploy --to lxd:3 --channel 2023.2/stable --config ncc.yaml nova-cloud-controller

       juju deploy --to 14  --channel 2023.2/stable --config ncc.yaml nova-cloud-controller
       juju deploy --channel 8.0/stable mysql-router ncc-mysql-router
       juju integrate ncc-mysql-router:db-router mysql-innodb-cluster:db-router
       juju integrate ncc-mysql-router:shared-db nova-cloud-controller:shared-db

       juju integrate nova-cloud-controller:identity-service keystone:identity-service
       juju integrate nova-cloud-controller:amqp rabbitmq-server:amqp
       juju integrate nova-cloud-controller:neutron-api neutron-api:neutron-api
       juju integrate nova-cloud-controller:cloud-compute nova-compute:cloud-compute
       juju integrate nova-cloud-controller:certificates vault:certificates


10. deploy placement

        # juju deploy --to lxd:3 --channel 2023.2/stable placement
        juju deploy --to 15 --channel 2023.2/stable placement
        juju deploy --channel 8.0/stable mysql-router placement-mysql-router
        juju integrate placement-mysql-router:db-router mysql-innodb-cluster:db-router
        juju integrate placement-mysql-router:shared-db placement:shared-db
        juju integrate placement:identity-service keystone:identity-service
        juju integrate placement:placement nova-cloud-controller:placement
        juju integrate placement:certificates vault:certificates

11. deploy openstack dashboard

        #juju deploy --to lxd:2 --channel 2023.2/stable openstack-dashboard
        juju deploy --to 16 --channel 2023.2/stable openstack-dashboard
        juju deploy --channel 8.0/stable mysql-router dashboard-mysql-router
        juju integrate dashboard-mysql-router:db-router mysql-innodb-cluster:db-router
        juju integrate dashboard-mysql-router:shared-db openstack-dashboard:shared-db
        juju integrate openstack-dashboard:identity-service keystone:identity-service
        juju integrate openstack-dashboard:certificates vault:certificates

12. deploy glance

        # juju deploy --to lxd:3 --channel 2023.2/stable glance
        juju deploy --to 17 --channel 2023.2/stable glance
        juju deploy --channel 8.0/stable mysql-router glance-mysql-router
        juju integrate glance-mysql-router:db-router mysql-innodb-cluster:db-router
        juju integrate glance-mysql-router:shared-db glance:shared-db
        juju integrate glance:image-service nova-cloud-controller:image-service
        juju integrate glance:image-service nova-compute:image-service
        juju integrate glance:identity-service keystone:identity-service
        juju integrate glance:certificates vault:certificates

13. deploy ceph-monitor

        cat << EOF | tee ceph-mon.yaml
        ceph-mon:
          expected-osd-count: 4
          monitor-count: 3
         EOF

        # juju deploy -n 3 --to lxd:0,lxd:1,lxd:2 --channel reef/stable --config ceph-mon.yaml ceph-mon
        juju deploy -n 3 --to 18,19,20 --channel reef/stable --config ceph-mon.yaml ceph-mon
        juju integrate ceph-mon:osd ceph-osd:mon
        juju integrate ceph-mon:client nova-compute:ceph
        juju integrate ceph-mon:client glance:ceph

14. deploy cinder monitor

        cat << EOF | tee cinder.yaml
        cinder:
          block-device: None
          glance-api-version: 2
        EOF

        # juju deploy --to lxd:1 --channel 2023.2/stable --config cinder.yaml cinder
        juju deploy --to 21 --channel 2023.2/stable --config cinder.yaml cinder
        juju deploy --channel 8.0/stable mysql-router cinder-mysql-router
        juju integrate cinder-mysql-router:db-router mysql-innodb-cluster:db-router
        juju integrate cinder-mysql-router:shared-db cinder:shared-db
        juju integrate cinder:cinder-volume-service nova-cloud-controller:cinder-volume-service
        juju integrate cinder:identity-service keystone:identity-service
        juju integrate cinder:amqp rabbitmq-server:amqp
        juju integrate cinder:image-service glance:image-service
        juju integrate cinder:certificates vault:certificates
        juju deploy --channel 2023.2/stable cinder-ceph 
        juju integrate cinder-ceph:storage-backend cinder:storage-backend
        juju integrate cinder-ceph:ceph ceph-mon:client
        juju integrate cinder-ceph:ceph-access nova-compute:ceph-access  

15. Deploy RADOS Gateway

        # juju deploy --to lxd:0 --channel reef/stable ceph-radosgw
        juju deploy --to 22 --channel reef/stable ceph-radosgw

        juju integrate ceph-radosgw:mon ceph-mon:radosgw 

16. recover from reboot

        juju run mysql-innodb-cluster/1 reboot-cluster-from-complete-outage

17. enable VNC access to VM

        juju config nova-cloud-controller console-access-protocol=novnc

18. enable port security on openstack

        juju config neutron-api enable-ml2-port-security=True

19. Install openstack clients

        sudo snap install openstackclients

11. Download openrc from [this](https://docs.openstack.org/project-deploy-guide/charm-deployment-guide/latest/_downloads/c894c4911b9572f0b5f86bdfc5d12d8e/openrc)

        curl -L -O https://docs.openstack.org/project-deploy-guide/charm-deployment-guide/latest/_downloads/c894c4911b9572f0b5f86bdfc5d12d8e/openrc

12. source openrc to use openstack client

        source openrc

