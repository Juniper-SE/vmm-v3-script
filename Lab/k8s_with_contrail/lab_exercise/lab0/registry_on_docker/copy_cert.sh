#!/bin/bash
for i in master node{1..3}
do
  scp certs/registry.crt ${i}:~/
  ssh ${i} "sudo mkdir  -p /etc/docker/certs.d/172.16.14.10:5000; sudo cp ~/registry.crt /etc/docker/certs.d/172.16.14.10:5000/ca.crt"
done
