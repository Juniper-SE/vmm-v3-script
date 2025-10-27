#!/bin/bash

# creating client for site 1 and 3
for i in 1 3
do
for ip1 in 101 102
do
LANBR=lab2cust3ce${i}
LXC=lab2cust3cl${i}-${ip1}
echo "create ${LXC} "
lxc copy router ${LXC}
echo "changing container ${LXC}"
lxc query --request PATCH /1.0/instances/${LXC} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${LANBR}\",
       \"type\": \"nic\"
    }
  }
}"

echo "changing container ${LXC}"
cat << EOF | tee interfaces
auto eth0
iface eth0 inet static
    address 172.16.1${i}.${ip1}/24
    gateway 172.16.1${i}.1
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:a01${i}::1000:${ip1}/64
    gateway fc00:dead:beef:a01${i}::1
EOF

echo "push configuration into node ${LXC}"
lxc file push interfaces  ${LXC}/etc/network/interfaces

# cat << EOF | tee resolv.conf
# nameserver 172.16.210.1
# EOF
# lxc file push resolv.conf ${LXC}/etc/resolv.conf

lxc start ${LXC}

cat << EOF | tee -a hosts
127.0.0.1	localhost localhost.localdomain
::1		localhost localhost.localdomain
172.16.11.101 lab2cust3cl1-101
172.16.11.102 lab2cust3cl1-102
172.16.12.101 lab2cust3cl2-101
172.16.12.102 lab2cust3cl2-102
172.16.13.101 lab2cust3cl3-101
172.16.13.102 lab2cust3cl3-102
172.16.12.103 lab2cust3cl4-103
172.16.12.104 lab2cust3cl4-104


fc00:dead:beef:a011::1000:101 lab2cust3cl1-101
fc00:dead:beef:a011::1000:102 lab2cust3cl1-102
fc00:dead:beef:a012::1000:101 lab2cust3cl2-101
fc00:dead:beef:a012::1000:102 lab2cust3cl2-102
fc00:dead:beef:a013::1000:101 lab2cust3cl3-101
fc00:dead:beef:a013::1000:102 lab2cust3cl3-102
fc00:dead:beef:a012::1000:103 lab2cust3cl4-103
fc00:dead:beef:a012::1000:104 lab2cust3cl4-104

EOF
echo "push configuration into node ${LXC}"
lxc file push hosts  ${LXC}/etc/hosts
echo "file uploaded"

done
done


for ip1 in 101 102
do
LANBR=pe2ge0
LXC=lab2cust3cl2-${ip1}
VLAN=110
echo "create ${LXC} "
lxc copy router ${LXC}
echo "changing container ${LXC}"
lxc query --request PATCH /1.0/instances/${LXC} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${LANBR}\",
       \"vlan\" : \"${VLAN}\",
       \"type\": \"nic\"
    }
  }
}"

echo "changing container ${LXC}"
cat << EOF | tee interfaces
auto eth0
iface eth0 inet static
    address 172.16.12.${ip1}/24
    gateway 172.16.12.1
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:a012::1000:${ip1}/64
    gateway fc00:dead:beef:a012::1
EOF

echo "push configuration into node ${LXC}"
lxc file push interfaces  ${LXC}/etc/network/interfaces

# cat << EOF | tee resolv.conf
# nameserver 172.16.210.1
# EOF
# lxc file push resolv.conf ${LXC}/etc/resolv.conf

lxc start ${LXC}

cat << EOF | tee -a hosts
127.0.0.1	localhost localhost.localdomain
::1		localhost localhost.localdomain
172.16.11.101 lab2cust3cl1-101
172.16.11.102 lab2cust3cl1-102
172.16.12.101 lab2cust3cl2-101
172.16.12.102 lab2cust3cl2-102
172.16.13.101 lab2cust3cl3-101
172.16.13.102 lab2cust3cl3-102
172.16.12.103 lab2cust3cl4-103
172.16.12.104 lab2cust3cl4-104


fc00:dead:beef:a011::1000:101 lab2cust3cl1-101
fc00:dead:beef:a011::1000:102 lab2cust3cl1-102
fc00:dead:beef:a012::1000:101 lab2cust3cl2-101
fc00:dead:beef:a012::1000:102 lab2cust3cl2-102
fc00:dead:beef:a013::1000:101 lab2cust3cl3-101
fc00:dead:beef:a013::1000:102 lab2cust3cl3-102
fc00:dead:beef:a012::1000:103 lab2cust3cl4-103
fc00:dead:beef:a012::1000:104 lab2cust3cl4-104

EOF
echo "push configuration into node ${LXC}"
lxc file push hosts  ${LXC}/etc/hosts
echo "file uploaded"

done



for ip1 in 103 104
do
LANBR=pe4ge0
LXC=lab2cust3cl4-${ip1}
VLAN=110
echo "create ${LXC} "
lxc copy router ${LXC}
echo "changing container ${LXC}"
lxc query --request PATCH /1.0/instances/${LXC} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${LANBR}\",
       \"vlan\" : \"${VLAN}\",
       \"type\": \"nic\"
    }
  }
}"

echo "changing container ${LXC}"
cat << EOF | tee interfaces
auto eth0
iface eth0 inet static
    address 172.16.12.${ip1}/24
    gateway 172.16.12.1
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:a012::1000:${ip1}/64
    gateway fc00:dead:beef:a012::1
EOF

echo "push configuration into node ${LXC}"
lxc file push interfaces  ${LXC}/etc/network/interfaces

# cat << EOF | tee resolv.conf
# nameserver 172.16.210.1
# EOF
# lxc file push resolv.conf ${LXC}/etc/resolv.conf

lxc start ${LXC}

cat << EOF | tee -a hosts
127.0.0.1	localhost localhost.localdomain
::1		localhost localhost.localdomain
172.16.11.101 lab2cust3cl1-101
172.16.11.102 lab2cust3cl1-102
172.16.12.101 lab2cust3cl2-101
172.16.12.102 lab2cust3cl2-102
172.16.13.101 lab2cust3cl3-101
172.16.13.102 lab2cust3cl3-102
172.16.12.103 lab2cust3cl4-103
172.16.12.104 lab2cust3cl4-104


fc00:dead:beef:a011::1000:101 lab2cust3cl1-101
fc00:dead:beef:a011::1000:102 lab2cust3cl1-102
fc00:dead:beef:a012::1000:101 lab2cust3cl2-101
fc00:dead:beef:a012::1000:102 lab2cust3cl2-102
fc00:dead:beef:a013::1000:101 lab2cust3cl3-101
fc00:dead:beef:a013::1000:102 lab2cust3cl3-102
fc00:dead:beef:a012::1000:103 lab2cust3cl4-103
fc00:dead:beef:a012::1000:104 lab2cust3cl4-104

EOF
echo "push configuration into node ${LXC}"
lxc file push hosts  ${LXC}/etc/hosts
echo "file uploaded"

done