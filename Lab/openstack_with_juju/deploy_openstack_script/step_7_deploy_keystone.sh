#!/bin/bash
# juju deploy --to lxd:0 --channel 2023.2/stable keystone

juju deploy --to 12  --channel 2023.2/stable keystone

juju deploy --channel 8.0/stable mysql-router keystone-mysql-router
juju integrate keystone-mysql-router:db-router mysql-innodb-cluster:db-router
juju integrate keystone-mysql-router:shared-db keystone:shared-db

juju integrate keystone:identity-service neutron-api:identity-service
juju integrate keystone:certificates vault:certificates
