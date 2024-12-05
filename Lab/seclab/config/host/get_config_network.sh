#!/bin/bash
for i in server1 client1a client1b client2 client3 client4 external
do
  scp ${i}:/etc/netplan/02_net.yaml ${i}_02_net.yaml
done
