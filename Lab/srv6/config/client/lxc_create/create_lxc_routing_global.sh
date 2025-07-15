#!/bin/bash
for i in {1..4}
do 
    echo "creating LXC s${i}ce1"
    lxc copy router s${i}ce1
    echo "creating LXC s${i}ce1c1"
    lxc copy client s${i}ce1c1
done 

# changing LXC container configuration, node router
VLAN=101
for i in {1..4}
do
OVS=ovs${i}
BR=s${i}ce1eth1
echo "changing container s${i}ce1"
lxc query --request PATCH /1.0/instances/s${i}ce1 --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${OVS}\",
       \"vlan\" : \"${VLAN}\",
       \"type\": \"nic\"
    },
    \"eth1\" :{
       \"name\": \"eth1\",
       \"nictype\": \"bridged\",
       \"parent\": \"${BR}\",
       \"type\": \"nic\"
    }
  }
}"

echo "changing container s${i}ce1c1"
lxc query --request PATCH /1.0/instances/s${i}ce1c1 --data "{
\"devices\": {
        \"eth0\" : {
            \"name\": \"eth0\",
            \"nictype\": \"bridged\",
            \"parent\": \"${BR}\",
            \"type\": \"nic\"
        }
    }
}"
done

# Changing lxc container configuration, node client

EP=0
RP=1
for i in {1..4}
do 
NET=10${i}
ASN=100${i}
echo "changing container s${i}ce1"
cat << EOF | tee interfaces
auto eth0
iface eth0 inet static
    address 192.168.255.${EP}/31
    mtu 1500
auto eth1
iface eth1 inet static
    address 192.168.${NET}.1/24
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:ffff::${EP}/127
iface eth1 inet6 static
    address fc00:dead:beef:a${NET}::1/64
EOF

cat << EOF | tee frr.conf 
frr defaults traditional
hostname s${i}ce1
log syslog informational
ipv6 forwarding
service integrated-vtysh-config
!
interface eth1
 ipv6 nd prefix fc00:dead:beef:a${NET}::/64
 no ipv6 nd suppress-ra
exit
router bgp 420000${ASN}
 no bgp ebgp-requires-policy
 neighbor 192.168.255.${RP} remote-as 4200000001
 neighbor fc00:dead:beef:ffff::${RP} remote-as 4200000001
 !
 address-family ipv4 unicast
  network 192.168.${NET}.0/24
 exit-address-family
 !
 address-family ipv6 unicast
  network fc00:dead:beef:a${NET}::/64
  neighbor fc00:dead:beef:ffff::${RP} activate
 exit-address-family
exit
!
EOF

EP=$(($EP + 2))
RP=$(($RP + 2))

cat << EOF | tee dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
log-facility local7;
subnet 192.168.${NET}.0 netmask 255.255.255.0 {
  range 192.168.${NET}.101 192.168.${NET}.200;
  option routers 192.168.${NET}.1;
}
EOF

echo "push configuration into node s${i}ce1"
lxc file push interfaces s${i}ce1/etc/network/interfaces
lxc file push frr.conf s${i}ce1/etc/frr/frr.conf
lxc file push dhcpd.conf s${i}ce1/etc/dhcp/dhcpd.conf

done

for i in {1..4}
do
    lxc start s${i}ce1
    lxc start s${i}ce1c1
done

