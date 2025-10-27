#!/bin/bash
for i in {1..3}
do
for ip1 in 1 2
do
LANBR=pe${i}ge0
LXC=lab2cust2cl${i}${ip1}
VLAN=103
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
    address 172.16.220.${i}${ip1}/24
    gateway 172.16.220.1
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:a220::1000:${i}${ip1}/64
    gateway fc00:dead:beef:a220::1
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
172.16.220.11 lab2cust2cl11
172.16.220.12 lab2cust2cl12
172.16.220.21 lab2cust2cl21
172.16.220.22 lab2cust2cl22
172.16.220.31 lab2cust2cl31
172.16.220.32 lab2cust2cl32

fc00:dead:beef:a220::1000:11 lab2cust2cl11
fc00:dead:beef:a220::1000:12 lab2cust2cl12
fc00:dead:beef:a220::1000:21 lab2cust2cl21
fc00:dead:beef:a220::1000:22 lab2cust2cl22
fc00:dead:beef:a220::1000:31 lab2cust2cl31
fc00:dead:beef:a220::1000:32 lab2cust2cl32

EOF
echo "push configuration into node ${LXC}"
lxc file push hosts  ${LXC}/etc/hosts
echo "file uploaded"

done
done