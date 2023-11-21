#!/bin/bash
# 172.16.14.10 is the ip address of the registry 
REGISTRY_IP=172.16.14.10
for i in node{0..3}
do
        scp ~/registry/certs/registry.crt ${i}:~/
        ssh ${i} "sudo cp ~/registry.crt /etc/ssl/certs/" 
done
sudo mkdir -p /etc/containers/certs.d/172.16.14.10:5000/
sudo cp ~/registry/certs/registry.crt /etc/containers/certs.d/172.16.14.10:5000/ca.crt
