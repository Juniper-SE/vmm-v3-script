# configuring router
# export LXC_NAME=ce1-pe11
# export VLANWAN=101
# export OVSWAN=pe11et0
# export IPv4WAN=172.16.255.1/31
# export IPv6WAN=fc00:dead:beef:ffff::1/127
# export VLANLAN=1101
# export OVSLAN=cpe
# export IPv4LAN=192.168.101.1/24
# export IPv6LAN=fc00:dead:beef:1101::1/64
# export ASN=4200001001
# export BGPIPv4REMOTE=172.16.255.0 
# export BGPIPv6REMOTE=fc00:dead:beef:ffff::0
# export ASN_REMOTE=4200000001
# export ADV_IPV4=192.168.101.0/24
# export ADV_IPV6=fc00:dead:beef:1101::/64

# export LXC_NAME=ce2-pe12
# export VLANWAN=101
# export OVSWAN=pe12et0
# export IPv4WAN=172.16.255.3/31
# export IPv6WAN=fc00:dead:beef:ffff::3/127
# export VLANLAN=1102
# export OVSLAN=cpe
# export IPv4LAN=192.168.102.1/24
# export IPv6LAN=fc00:dead:beef:1102::1/64
# export ASN=4200001002
# export BGPIPv4REMOTE=172.16.255.2
# export BGPIPv6REMOTE=fc00:dead:beef:ffff::2
# export ASN_REMOTE=4200000001
# export ADV_IPV4=192.168.102.0/24
# export ADV_IPV6=fc00:dead:beef:1102::/64

# export LXC_NAME=ce3-pe13
# export VLANWAN=101
# export OVSWAN=pe13et0
# export IPv4WAN=172.16.255.5/31
# export IPv6WAN=fc00:dead:beef:ffff::5/127
# export VLANLAN=1103
# export OVSLAN=cpe
# export IPv4LAN=192.168.103.1/24
# export IPv6LAN=fc00:dead:beef:1103::1/64
# export ASN=4200001003
# export BGPIPv4REMOTE=172.16.255.4
# export BGPIPv6REMOTE=fc00:dead:beef:ffff::4
# export ASN_REMOTE=4200000001
# export ADV_IPV4=192.168.103.0/24
# export ADV_IPV6=fc00:dead:beef:1103::/64

export LXC_NAME=ce4-pe14
export VLANWAN=101
export OVSWAN=pe14ge0
export IPv4WAN=172.16.255.7/31
export IPv6WAN=fc00:dead:beef:ffff::7/127
export VLANLAN=1104
export OVSLAN=cpe
export IPv4LAN=192.168.104.1/24
export IPv6LAN=fc00:dead:beef:1104::1/64
export ASN=4200001004
export BGPIPv4REMOTE=172.16.255.6
export BGPIPv6REMOTE=fc00:dead:beef:ffff::6
export ASN_REMOTE=4200000001
export ADV_IPV4=192.168.104.0/24
export ADV_IPV6=fc00:dead:beef:1104::/64


echo "Creating VM ${LXC_NAME}"
lxc copy router ${LXC_NAME}
lxc query --request PATCH /1.0/instances/${LXC_NAME} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${OVSWAN}\",
       \"vlan\" : \"${VLANWAN}\",
       \"type\": \"nic\"
    },
    \"eth1\" :{
       \"name\": \"eth1\",
       \"nictype\": \"bridged\",
       \"parent\": \"${OVSLAN}\",
       \"vlan\" : \"${VLANLAN}\",
       \"type\": \"nic\"
    }
  }
}"
echo "push configuration into node ${LXC_NAME}"
cat << EOF | tee ./interface.conf
auto eth0
iface eth0 inet static
    address ${IPv4WAN}
iface eth0 inet6 static
    address ${IPv6WAN}
auto eth1
iface eth1 inet static
    address ${IPv4LAN}
iface eth1 inet6 static
    address ${IPv6LAN}
EOF

lxc file push ./interface.conf ${LXC_NAME}/etc/network/interfaces


cat << EOF | tee ./frr.conf
frr defaults traditional
hostname c1-pe11
log syslog informational
service integrated-vtysh-config
!
router bgp ${ASN}
 no bgp ebgp-requires-policy
 neighbor ${BGPIPv4REMOTE} remote-as ${ASN_REMOTE}
 neighbor ${BGPIPv6REMOTE} remote-as ${ASN_REMOTE}
 !
 address-family ipv4 unicast
  network ${ADV_IPV4}
 exit-address-family
 !
 address-family ipv6 unicast
  network ${ADV_IPV6}
  neighbor ${BGPIPv6REMOTE} activate
 exit-address-family
exit
EOF

lxc file push ./frr.conf ${LXC_NAME}/etc/frr/frr.conf
lxc start ${LXC_NAME}