#!/bin/bash
for i in master node{1..3}
do
  scp registry/certs/registry.crt ${i}:~/
  ssh ${i} "sudo mkdir  -p /etc/containers/certs.d/10.1.1.200:5000; sudo cp ~/registry.crt /etc/containers/certs.d/10.1.1.200:5000/ca.crt"
done
