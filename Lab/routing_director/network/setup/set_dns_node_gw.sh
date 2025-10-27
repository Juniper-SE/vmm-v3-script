#!/bin/bash
cat << EOF | sudo tee -a /etc/coredns/vmmlab.com.db
pe1 IN A 10.100.255.1
pe2 IN A 10.100.255.2
pe3 IN A 10.100.255.3
pe4 IN A 10.100.255.4
pe5 IN A 10.100.255.5
p1 IN A 10.100.255.11
p2 IN A 10.100.255.12
p3 IN A 10.100.255.13
p4 IN A 10.100.255.14
p5 IN A 10.100.255.15
crpd IN A 10.100.255.10
EOF
sudo systemctl restart coredns
