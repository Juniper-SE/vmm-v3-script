#!/bin/bash
for i in svr{1..9} lxc{1..2}
do
  scp ${i}:/etc/netplan/02_net.yaml ${i}_02_net.yaml
done

