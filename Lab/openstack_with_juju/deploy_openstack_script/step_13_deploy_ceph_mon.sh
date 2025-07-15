#!/bin/bash
# juju deploy -n 3 --to lxd:0,lxd:1,lxd:2 --channel reef/stable --config ceph-mon.yaml ceph-mon
juju deploy -n 3 --to 18,19,20 --channel reef/stable --config ceph-mon.yaml ceph-mon
juju integrate ceph-mon:osd ceph-osd:mon
juju integrate ceph-mon:client nova-compute:ceph
juju integrate ceph-mon:client glance:ceph