#!/bin/bash
sudo systemctl stop sshd
sudo rm /etc/ssh/ssh_host*
sudo ssh-keygen -q -f /etc/ssh/ssh_host_key -N '' -t rsa1
sudo ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
sudo ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa
sudo ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa -b 521
sudo systemctl restart sshd
#sudo fdisk -l /dev/sda
echo "n


64G
n


40G
w
q
" | sudo fdisk /dev/sda

cat << EOF | sudo tee /etc/hosts
127.0.0.1 localhost
172.16.11.200 deployer
172.16.11.111 node1
172.16.11.112 node2
172.16.11.113 node3

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
EOF

rm ~/.ssh/*

sudo mkfs.ext4 /dev/sda2
sudo mkfs.ext4 /dev/sda3

ss
