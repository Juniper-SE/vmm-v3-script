#!/bin/bash
for i in 162 166 168 176 178
do 
export LXC_NAME=lxc-$i
echo "push configuration into node ${LXC_NAME}"
cat << EOF | tee 50-cloud-init.yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      addresses: 
      - 172.16.11.${i}/24
      routes:
      - to: default
        via: 172.16.11.1
      nameservers:
        addresses:
        - 10.49.32.95
        - 10.94.32.97
EOF
lxc file push /home/ubuntu/50-cloud-init.yaml ${LXC_NAME}/etc/netplan/50-cloud-init.yaml
lxc file push /home/ubuntu/.ssh/id_rsa.pub ${LXC_NAME}/root/.ssh/authorized_keys
lxc restart ${LXC_NAME}
done