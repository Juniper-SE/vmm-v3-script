#!/bin/bash
for i in master node{1..3}
do
  scp registry/certs/registry.crt ${i}:~/
  ssh ${i} "sudo mkdir  -p /etc/containers/certs.d/172.16.14.10:5000; sudo cp ~/registry.crt /etc/containers/certs.d/172.16.14.10:5000/ca.crt"
  # ssh ${i} "sudo mkdir  -p /etc/docker/certs.d/172.16.14.10:5000; sudo cp ~/registry.crt /etc/docker/certs.d/172.16.14.10:5000/ca.crt"
  #ssh ${i} "sudo cp ~/registry.crt /usr/local/share/ca-certificates/172.16.14.10-5000.ca.crt; sudo update-ca-certificates"
done
sudo mkdir  -p /etc/containers/certs.d/172.16.14.10:5000
sudo cp ~/registry/certs/registry.crt /etc/containers/certs.d/172.16.14.10:5000/ca.crt
#sudo cp ~/registry.crt /usr/local/share/ca-certificates/172.16.14.10-5000.ca.crt; sudo update-ca-certificates
#sudo update-ca-certificates
