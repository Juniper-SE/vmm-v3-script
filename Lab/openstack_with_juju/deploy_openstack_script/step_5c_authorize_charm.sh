#!/bin/bash
export TOKEN=
juju run  vault/leader authorize-charm token=${TOKEN}
juju run vault/leader generate-root-ca
juju integrate mysql-innodb-cluster:certificates vault:certificates