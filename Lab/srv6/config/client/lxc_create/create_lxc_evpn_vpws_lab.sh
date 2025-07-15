#!/bin/bash
for i in {1..4}
do 
    echo "creating LXC s${i}ce3"
    lxc copy router s${i}ce3
    echo "creating LXC s${i}ce3c1"
    lxc copy client s${i}ce3c1
done 

# changing LXC container configuration, node router
VLAN=111
for i in {2..4}
do
OVS=ovs${i}
BR=s${i}ce3eth1
echo "changing container s${i}ce3"
lxc query --request PATCH /1.0/instances/s${i}ce3 --data "{
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
VLAN=$(($VLAN + 1))
done
echo "changing container s1ce3"
lxc query --request PATCH /1.0/instances/s1ce3 --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"s1ce3eth1\",
       \"type\": \"nic\"
    },
    \"eth1\" :{
       \"name\": \"eth1\",
       \"nictype\": \"bridged\",
       \"parent\": \"ovs1\",
       \"vlan\" : \"111\",
       \"type\": \"nic\"
    },
    \"eth2\" :{
       \"name\": \"eth2\",
       \"nictype\": \"bridged\",
       \"parent\": \"ovs1\",
       \"vlan\" : \"112\",
       \"type\": \"nic\"
    },
    \"eth3\" :{
       \"name\": \"eth3\",
       \"nictype\": \"bridged\",
       \"parent\": \"ovs1\",
       \"vlan\" : \"113\",
       \"type\": \"nic\"
    }
  }
}"

for i in {1..4}
do
BR=s${i}ce3eth1
echo "changing container s${i}ce3c1"
lxc query --request PATCH /1.0/instances/s${i}ce3c1 --data "{
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
#!/bin/bash
echo "changing container s1ce3"
cat << EOF | tee interfaces
auto eth0
iface eth0 inet static
    mtu 1500
    address 192.168.121.1/24
iface eth0 inet6 static
    mtu 1500
    address fc00:dead:beef:a121::1/64
auto eth1
iface eth1 inet static
    address 192.168.255.0/31
iface eth1 inet6 static
    address fc00:dead:beef:ffff::0/127
auto eth2
iface eth2 inet static
    address 192.168.255.2/31
iface eth2 inet6 static
    address fc00:dead:beef:ffff::2/127
auto eth3
iface eth3 inet static
    address 192.168.255.4/31
iface eth3 inet6 static
    address fc00:dead:beef:ffff::4/127
EOF

cat << EOF | tee frr.conf 
frr defaults traditional
hostname s1ce3
log syslog informational
ipv6 forwarding
service integrated-vtysh-config
!
interface eth0
 ipv6 nd prefix fc00:dead:beef:a121::/64
 no ipv6 nd suppress-ra
exit
router bgp 1
 no bgp ebgp-requires-policy
 neighbor 192.168.255.1 remote-as 2
 neighbor 192.168.255.3 remote-as 3
 neighbor 192.168.255.5 remote-as 4
 neighbor fc00:dead:beef:ffff::1 remote-as 2
 neighbor fc00:dead:beef:ffff::3 remote-as 3
 neighbor fc00:dead:beef:ffff::5 remote-as 4
 !
 address-family ipv4 unicast
  redistribute connected
 exit-address-family
 !
 address-family ipv6 unicast
  network fc00:dead:beef:a121::/64
  redistribute connected
  neighbor fc00:dead:beef:ffff::1 activate
  neighbor fc00:dead:beef:ffff::3 activate
  neighbor fc00:dead:beef:ffff::5 activate
 exit-address-family
exit
!
EOF

cat << EOF | tee dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
log-facility local7;
subnet 192.168.121.0 netmask 255.255.255.0 {
  range 192.168.121.101 192.168.121.200;
  option routers 192.168.121.1;
}
EOF

lxc file pull s1ce3/etc/frr/daemons frr.daemons
sed -i -e "s/bgpd=no/bgpd=yes/" frr.daemons
lxc file push interfaces s1ce3/etc/network/interfaces
lxc file push frr.conf s1ce3/etc/frr/frr.conf
lxc file push frr.daemons s1ce3/etc/frr/daemons
lxc file push dhcpd.conf s1ce3/etc/dhcp/dhcpd.conf

EP=1
ASN=2
BGP=0
for i in {2..4}
do
echo "changing container s${i}ce3"
cat << EOF | tee interfaces
auto eth1
iface eth1 inet static
    mtu 1500
    address 192.168.12${i}.1/24
iface eth1 inet6 static
    mtu 1500
    address fc00:dead:beef:a12${i}::1/64
auto eth0
iface eth0 inet static
    address 192.168.255.${EP}/31
iface eth0 inet6 static
    address fc00:dead:beef:ffff::${EP}/127
EOF

EP=$((${EP}+2))

cat << EOF | tee frr.conf 
frr defaults traditional
hostname s${i}ce3
log syslog informational
ipv6 forwarding
service integrated-vtysh-config
!
interface eth1
 ipv6 nd prefix fc00:dead:beef:a12${i}::/64
 no ipv6 nd suppress-ra
exit
router bgp ${ASN}
 no bgp ebgp-requires-policy
 neighbor 192.168.255.${BGP} remote-as 1
 neighbor fc00:dead:beef:ffff::${BGP} remote-as 1
 !
 address-family ipv4 unicast
  redistribute connected
 exit-address-family
 !
 address-family ipv6 unicast
  redistribute connected
  neighbor fc00:dead:beef:ffff::${BGP} activate
 exit-address-family
exit
!
EOF

ASN=$((${ASN}+1))
BGP=$((${BGP}+2))

cat << EOF | tee dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
log-facility local7;
subnet 192.168.12${i}.0 netmask 255.255.255.0 {
  range 192.168.12${i}.101 192.168.12${i}.200;
  option routers 192.168.12${i}.1;
}
EOF

lxc file pull s${i}ce3/etc/frr/daemons frr.daemons
sed -i -e "s/bgpd=no/bgpd=yes/" frr.daemons
lxc file push interfaces s${i}ce3/etc/network/interfaces
lxc file push frr.conf s${i}ce3/etc/frr/frr.conf
lxc file push frr.daemons s${i}ce3/etc/frr/daemons
lxc file push dhcpd.conf s${i}ce3/etc/dhcp/dhcpd.conf
done

lxc start s{1..4}ce3
lxc start s{1..4}ce3c1


# lxc stop s{1..4}ce3
# lxc stop s{1..4}ce3c1
# lxc rm s{1..4}ce3
# lxc rm s{1..4}ce3c1

