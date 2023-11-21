#!/bin/bash
# 172.16.14.10 is the ip address of the registry 
REGISTRY_IP=172.16.14.10
for i in master node{1..3}
do
   scp certs/registry.crt ${i}:~/
   ssh ${i} "sudo mkdir  -p /etc/containers/certs.d/${REGISTRY_IP}:5000; sudo cp ~/registry.crt /etc/containers/certs.d/${REGISTRY_IP}:5000/ca.crt" 
done
