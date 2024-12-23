# deploying openstack using charm

## configure juju controller

1. login into node client, and install juju client

       sudo snap install juju

2. create/bootstrap juju controller on node juju (172.16.11.101)

       juju bootstrap manual/ubuntu@172.16.11.101 vmm
       juju add-model --config default-series=jammy openstack

3. Add host (node0, node1, node2, node3) into the controller

       juju add-machine ssh:ubuntu@172.16.11.110
       juju add-machine ssh:ubuntu@172.16.11.111
       juju add-machine ssh:ubuntu@172.16.11.112
       juju add-machine ssh:ubuntu@172.16.11.113


## deploy openstack
1. Deploy Ceph OSD

       cat << EOF | tee ceph-osd.yaml
       ceph-osd:
         osd-devices: /dev/vdb /dev/vdc
       EOF

       juju deploy -n 4 --to 0,1,2,3 --channel reef/stable --config ceph-osd.yaml --constraints ceph-osd

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

       juju deploy -n 3 --to lxd:0,lxd:1,lxd:2 --channel 8.0/stable mysql-innodb-cluster

4. Deploy vault

       juju deploy --to lxd:3 --channel 1.8/stable vault
       juju deploy --channel 8.0/stable mysql-router vault-mysql-router
       juju integrate vault-mysql-router:db-router mysql-innodb-cluster:db-router
       juju integrate vault-mysql-router:shared-db vault:shared-db
            
5. Initialize and unseal vault

       export VAULT_ADDR="http://192.168.110.9:8200"
       vault operator init -key-shares=5 -key-threshold=3

       vault operator unseal <key1>
       vault operator unseal <key2>
       vault operator unseal <key3>

       export VAULT_TOKEN=<initial_root_token>
       vault token create -ttl=10m
       juju run  vault/leader authorize-charm token=<token>
       juju run vault/leader generate-root-ca

       juju integrate mysql-innodb-cluster:certificates vault:certificates