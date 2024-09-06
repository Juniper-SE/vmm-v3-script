#!/bin/bash
CUST=c1
CLIENT=cl1
VLAN=101
for i in {1..4}
do 
    echo "creating LXC ${CUST}ce${i}"
    lxc copy router ${CUST}ce${i}
    echo "creating LXC ${CUST}ce${i}${CLIENT}"
    lxc copy client ${CUST}ce${i}${CLIENT}
done 

# changing LXC container configuration, node router
for i in {1..4}
do
OVS=pe${i}ge0
BR=${CUST}ce${i}eth1
echo "changing container ${CUST}ce${i}"
lxc query --request PATCH /1.0/instances/${CUST}ce${i} --data "{
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

echo "changing container ${CUST}ce${i}${CLIENT}"
lxc query --request PATCH /1.0/instances/${CUST}ce${i}${CLIENT} --data "{
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
EP=1
RP=0
for i in {1..4}
do 
NET=11${i}
ASN=200${i}
echo "changing container s${i}ce2"
cat << EOF | tee interfaces
auto eth0
iface eth0 inet static
    address 10.100.100.${EP}/31
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
hostname ${CUST}ce${i}
log syslog informational
ipv6 forwarding
service integrated-vtysh-config
!
interface eth1
 ipv6 nd prefix fc00:dead:beef:a${NET}::/64
 no ipv6 nd suppress-ra
exit
router bgp 420001${ASN}
 no bgp ebgp-requires-policy
 neighbor 10.100.100.${RP} remote-as 4200001001
 neighbor fc00:dead:beef:ffff::${RP} remote-as 4200001001
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

echo "push configuration into node ${CUST}ce${i}"
lxc file push interfaces  ${CUST}ce${i}/etc/network/interfaces
lxc file push frr.conf  ${CUST}ce${i}/etc/frr/frr.conf
lxc file push dhcpd.conf ${CUST}ce${i}/etc/dhcp/dhcpd.conf

done

for i in {1..4}
do
    lxc start ${CUST}ce${i}
    lxc start ${CUST}ce${i}${CLIENT}
done

