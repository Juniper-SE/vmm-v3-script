#!/bin/bash
juju deploy -n 3 --to 4,5,6 --channel 8.0/stable mysql-innodb-cluster
