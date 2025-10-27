#!/bin/bash
for i in 1 3
do
sudo ip link add dev lab2cust3ce${i} type bridge
sudo ip link set dev lab2cust3ce${i} up
done
ip1=0
for i in 1 3 
do
ip2=`expr ${ip1} + 1`
WANBR=pe${i}ge0
LANBR=lab2cust3ce${i}
VLAN=110
LXC=${LANBR}
echo "create ${LXC} "
lxc copy router ${LXC}
echo "changing container ${LXC}"
lxc query --request PATCH /1.0/instances/${LXC} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${WANBR}\",
       \"vlan\" : \"${VLAN}\",
       \"type\": \"nic\"
    },
    \"eth1\" :{
       \"name\": \"eth1\",
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
    address 172.16.220.${ip2}/31
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:a220::${ip2}/127
auto eth1
iface eth1 inet static
    address 172.16.1${i}.1/24
    mtu 1500
iface eth1 inet6 static
    address fc00:dead:beef:a01${i}::1/64
EOF
echo "push configuration into node ${LXC}"
lxc file push interfaces  ${LXC}/etc/network/interfaces

cat << EOF | tee frr.conf
ipv6 forwarding
router bgp 420000300${i}
 no bgp ebgp-requires-policy
 neighbor 172.16.220.${ip1} remote-as 4200000001
 neighbor fc00:dead:beef:a220::${ip1} remote-as 4200000001
 !
 address-family ipv4 unicast
  network 172.16.1${i}.0/24
 exit-address-family
 !
 address-family ipv6 unicast
  network fc00:dead:beef:a01${i}::/64
  neighbor fc00:dead:beef:a220::${ip1} activate
 exit-address-family
exit
EOF
lxc file push frr.conf  ${LXC}/etc/frr/frr.conf

ip1=`expr $ip1 + 2`

lxc start ${LXC}
done