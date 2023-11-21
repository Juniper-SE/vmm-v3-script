#!/bin/bash
for i in svr{1..9} lxc{1..2}
do
  echo "uploading config into $i"
  scp ${i}_02_net.yaml ${i}:~/02_net.yaml
  ssh ${i} "sudo cp ~/02_net.yaml /etc/netplan/02_net.yaml ; sudo netplan apply"
done

