#!/bin/ash
cat << EOF | sudo tee /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
127.0.1.1 br1
EOF

sudo rm /etc/local.d/*

cat << EOF | sudo tee /etc/hostname
br1
EOF

rm -rf ~/.ssh/
mkdir ~/.ssh

cat << EOF | tee ~/.ssh/authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDBUA+4YJwqE2rqwweZ3NG7GpXF3JqIxFbnDxraW8//QWjHLGVgn+jFbXFB3T/yLYpIRAh8SsAw6M6pZXzGd3oiltENLkoN5YGI1yW0bCTsS/Z4BoW/iuPR2rYQqhA+NPi9OZO/opVbJ+VIdfm+fugWPSVpduBiJN20P9iEF1zCW4EmWZn3qkl25LjVSBVMiwn+crcsCHUub3xDRicgTOOINFo4lZy03Fsa3PoqpxXv18FhNi3pVWmV2n3vIckWt8BbaPWMTFZmERHkVb4Y15GsHwcQxb6gm3h8Do4QgURbujCUJQhpJT4BRdD8kja1NQK4lbcPq6l9rF3YM7aQkscB16nCplWcgdnxI7eN//FA4ovvx7d57i43Y7GzSlQE87kcIDDQ1eCesYOfg9EfqCFSVWV0hbhc2Ap6YCoc0R9POpG1n0LO+o++h0J0bkLUWsIiQLb3LiC91FnP3giK5MEzdJ+maJcjIyGlTth52s01nLdT4gQDgTURqIpfL8L0HWE= irzan@irzan-mbp
EOF

cat << EOF | tee ~/.ssh/id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
EOF

sudo mkdir /root/.ssh
sudo cp ~/.ssh/id_rsa /root/.ssh/id_rsa
sudo cp ~/.ssh/authorized_keys /root/.ssh/authorized_keys



cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet static
   address 172.16.10.104/24
   gateway 172.16.10.254
   dns-nameservers 10.49.32.95 10.49.32.97 
   
 
auto eth1
iface eth1 inet manual
    mtu 9000
 
auto eth2
iface eth2 inet manual
    mtu 9000
 
auto eth3
iface eth3 inet manual
    mtu 9000
 
auto eth4
iface eth4 inet manual
    mtu 9000
 
auto eth5
iface eth5 inet manual
    mtu 9000
 
auto eth6
iface eth6 inet manual
    mtu 9000
 
auto eth7
iface eth7 inet manual
    mtu 9000
 
auto eth8
iface eth8 inet manual
    mtu 9000
 
auto eth9
iface eth9 inet manual
    mtu 9000
 
auto eth10
iface eth10 inet manual
    mtu 9000
 
auto eth11
iface eth11 inet manual
    mtu 9000
 
auto eth12
iface eth12 inet manual
    mtu 9000
 
auto eth13
iface eth13 inet manual
    mtu 9000
 
auto eth14
iface eth14 inet manual
    mtu 9000
 

EOF


uuidgen  | sed -e 's/-//g' |  sudo tee /etc/machine-id

cat << EOF | tee ~/.ssh/config
Host *
   StrictHostKeyChecking no
EOF

cat << EOF | sudo tee /etc/local.d/pe1p1.start
#!/bin/sh
ip link add dev pe1p1 type bridge
ip link set dev eth1 master pe1p1
ip link set dev eth2 master pe1p1

ip link set pe1p1 up
echo 0x4000 >  /sys/class/net/pe1p1/bridge/group_fwd_mask
EOF
sudo chmod +x /etc/local.d/pe1p1.start
cat << EOF | sudo tee /etc/local.d/pe1p2.start
#!/bin/sh
ip link add dev pe1p2 type bridge
ip link set dev eth3 master pe1p2
ip link set dev eth4 master pe1p2

ip link set pe1p2 up
echo 0x4000 >  /sys/class/net/pe1p2/bridge/group_fwd_mask
EOF
sudo chmod +x /etc/local.d/pe1p2.start
cat << EOF | sudo tee /etc/local.d/pe2p1.start
#!/bin/sh
ip link add dev pe2p1 type bridge
ip link set dev eth5 master pe2p1
ip link set dev eth6 master pe2p1

ip link set pe2p1 up
echo 0x4000 >  /sys/class/net/pe2p1/bridge/group_fwd_mask
EOF
sudo chmod +x /etc/local.d/pe2p1.start
cat << EOF | sudo tee /etc/local.d/pe2p2.start
#!/bin/sh
ip link add dev pe2p2 type bridge
ip link set dev eth7 master pe2p2
ip link set dev eth8 master pe2p2

ip link set pe2p2 up
echo 0x4000 >  /sys/class/net/pe2p2/bridge/group_fwd_mask
EOF
sudo chmod +x /etc/local.d/pe2p2.start
cat << EOF | sudo tee /etc/local.d/pe3p1.start
#!/bin/sh
ip link add dev pe3p1 type bridge
ip link set dev eth9 master pe3p1
ip link set dev eth10 master pe3p1

ip link set pe3p1 up
echo 0x4000 >  /sys/class/net/pe3p1/bridge/group_fwd_mask
EOF
sudo chmod +x /etc/local.d/pe3p1.start
cat << EOF | sudo tee /etc/local.d/pe3p2.start
#!/bin/sh
ip link add dev pe3p2 type bridge
ip link set dev eth11 master pe3p2
ip link set dev eth12 master pe3p2

ip link set pe3p2 up
echo 0x4000 >  /sys/class/net/pe3p2/bridge/group_fwd_mask
EOF
sudo chmod +x /etc/local.d/pe3p2.start
cat << EOF | sudo tee /etc/local.d/p1p2.start
#!/bin/sh
ip link add dev p1p2 type bridge
ip link set dev eth13 master p1p2
ip link set dev eth14 master p1p2

ip link set p1p2 up
echo 0x4000 >  /sys/class/net/p1p2/bridge/group_fwd_mask
EOF
sudo chmod +x /etc/local.d/p1p2.start

sudo rc-update add local default


chmod og-rwx ~/.ssh/*

sleep 2 
sudo reboot