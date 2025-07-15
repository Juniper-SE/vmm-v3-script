#!/bin/bash
juju deploy -n 4 --to 0,1,2,3 --channel reef/stable --config ceph-osd.yaml ceph-osd