#!/bin/bash
ip1=101
for i in {1..4}
do
for ip1 in 101 102
do
LANBR=lab1ce${i}
LXC=lab1cl${i}-${ip1}
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
    address 172.16.22${i}.${ip1}/24
    gateway 172.16.22${i}.1
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:a22${i}::1000:${ip1}/64
    gateway fc00:dead:beef:a22${i}::1
EOF

echo "push configuration into node ${LXC}"
lxc file push interfaces  ${LXC}/etc/network/interfaces

cat << EOF | tee resolv.conf
nameserver 172.16.210.1
EOF
lxc file push resolv.conf ${LXC}/etc/resolv.conf

lxc start ${LXC}

cat << EOF | tee -a hosts
127.0.0.1	localhost localhost.localdomain
::1		localhost localhost.localdomain
172.16.221.101 lab1cl1-101
172.16.221.102 lab1cl1-102
172.16.222.101 lab1cl2-101
172.16.222.102 lab1cl2-102
172.16.223.101 lab1cl3-101
172.16.223.102 lab1cl3-102
172.16.224.101 lab1cl4-101
172.16.224.102 lab1cl4-102

fc00:dead:beef:a221::1000:101 lab1cl1-101
fc00:dead:beef:a221::1000:102 lab1cl1-102
fc00:dead:beef:a222::1000:101 lab1cl2-101
fc00:dead:beef:a222::1000:102 lab1cl2-102
fc00:dead:beef:a223::1000:101 lab1cl3-101
fc00:dead:beef:a223::1000:102 lab1cl3-102
fc00:dead:beef:a224::1000:101 lab1cl4-101
fc00:dead:beef:a224::1000:101 lab1cl4-102
EOF
echo "push configuration into node ${LXC}"
lxc file push hosts  ${LXC}/etc/hosts
echo "file uploaded"

done
done