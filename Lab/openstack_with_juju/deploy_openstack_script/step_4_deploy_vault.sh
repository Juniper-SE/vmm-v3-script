#!/bin/bash
# juju deploy --to lxd:3 --channel 1.8/stable vault
juju deploy --to 7 --channel 1.8/stable vault
juju deploy --channel 8.0/stable mysql-router vault-mysql-router
juju integrate vault-mysql-router:db-router mysql-innodb-cluster:db-router
juju integrate vault-mysql-router:shared-db vault:shared-db