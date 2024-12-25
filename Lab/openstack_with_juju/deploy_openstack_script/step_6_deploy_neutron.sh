#!/bin/bash
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