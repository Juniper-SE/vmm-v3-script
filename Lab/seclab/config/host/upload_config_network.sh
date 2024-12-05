#!/bin/bash
for i in server1 client1a client1b client2 client3 client4 external
do
  scp  ./${i}_02_net.yaml ${i}:~/02_net.yaml
  ssh ${i} "sudo mv ~/02_net.yaml /etc/netplan/02_net.yaml; sudo netplan apply"
done
