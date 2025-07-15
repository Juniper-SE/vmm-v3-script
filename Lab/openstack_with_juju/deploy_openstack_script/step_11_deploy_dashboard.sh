#!/bin/bash
#juju deploy --to lxd:2 --channel 2023.2/stable openstack-dashboard
juju deploy --to 16 --channel 2023.2/stable openstack-dashboard
juju deploy --channel 8.0/stable mysql-router dashboard-mysql-router
juju integrate dashboard-mysql-router:db-router mysql-innodb-cluster:db-router
juju integrate dashboard-mysql-router:shared-db openstack-dashboard:shared-db
juju integrate openstack-dashboard:identity-service keystone:identity-service
juju integrate openstack-dashboard:certificates vault:certificates