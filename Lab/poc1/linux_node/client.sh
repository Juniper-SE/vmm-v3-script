# export LXC_NAME=cl1-ce1
# export VLANLAN=1101
# export OVSLAN=cpe
# export IPv4LAN=192.168.101.11/24
# export IPv4GW=192.168.101.1
# export IPv6LAN=fc00:dead:beef:1101::ffff:11/64
# export IPv6GW=fc00:dead:beef:1101::1

# export LXC_NAME=cl1-ce2
# export VLANLAN=1102
# export OVSLAN=cpe
# export IPv4LAN=192.168.102.11/24
# export IPv4GW=192.168.102.1
# export IPv6LAN=fc00:dead:beef:1102::ffff:11/64
# export IPv6GW=fc00:dead:beef:1102::1

# export LXC_NAME=cl1-ce3
# export VLANLAN=1103
# export OVSLAN=cpe
# export IPv4LAN=192.168.103.11/24
# export IPv4GW=192.168.103.1
# export IPv6LAN=fc00:dead:beef:1103::ffff:11/64
# export IPv6GW=fc00:dead:beef:1103::1

# export LXC_NAME=cl1-ce4
# export VLANLAN=1104
# export OVSLAN=cpe
# export IPv4LAN=192.168.104.11/24
# export IPv4GW=192.168.104.1
# export IPv6LAN=fc00:dead:beef:1104::ffff:11/64
# export IPv6GW=fc00:dead:beef:1104::1


# export LXC_NAME=cl1-evpn1
# export VLANLAN=111
# export OVSLAN=pe11et0
# export IPv4LAN=192.168.111.1/24
# export IPv4GW=192.168.111.254
# export IPv6LAN=fc00:dead:beef:1111::1/64
# export IPv6GW=fc00:dead:beef:1104::ffff:ffff

# export LXC_NAME=cl2-evpn1
# export VLANLAN=111
# export OVSLAN=pe12et0
# export IPv4LAN=192.168.111.2/24
# export IPv4GW=192.168.111.254
# export IPv6LAN=fc00:dead:beef:1111::2/64
# export IPv6GW=fc00:dead:beef:1104::ffff:ffff

# export LXC_NAME=cl3-evpn1
# export VLANLAN=112
# export OVSLAN=pe13et0
# export IPv4LAN=192.168.111.3/24
# export IPv4GW=192.168.111.254
# export IPv6LAN=fc00:dead:beef:1111::3/64
# export IPv6GW=fc00:dead:beef:1104::ffff:ffff

# export LXC_NAME=cl1-evpn2-201
# export VLANLAN=201
# export OVSLAN=pe11et0
# export IPv4LAN=192.168.201.1/24
# export IPv4GW=192.168.201.254
# export IPv6LAN=fc00:dead:beef:1201::1/64
# export IPv6GW=fc00:dead:beef:1201::ffff:ffff

# export LXC_NAME=cl1-evpn2-202
# export VLANLAN=202
# export OVSLAN=pe11et0
# export IPv4LAN=192.168.202.1/24
# export IPv4GW=192.168.202.254
# export IPv6LAN=fc00:dead:beef:1202::1/64
# export IPv6GW=fc00:dead:beef:1202::ffff:ffff

# export LXC_NAME=cl2-evpn2-201
# export VLANLAN=201
# export OVSLAN=pe12et0
# export IPv4LAN=192.168.201.2/24
# export IPv4GW=192.168.201.254
# export IPv6LAN=fc00:dead:beef:1201::2/64
# export IPv6GW=fc00:dead:beef:1201::ffff:ffff

# export LXC_NAME=cl2-evpn2-202
# export VLANLAN=202
# export OVSLAN=pe12et0
# export IPv4LAN=192.168.202.2/24
# export IPv4GW=192.168.202.254
# export IPv6LAN=fc00:dead:beef:1202::2/64
# export IPv6GW=fc00:dead:beef:1202::ffff:ffff

# export LXC_NAME=cl3-evpn2-201
# export VLANLAN=201
# export OVSLAN=pe13et0
# export IPv4LAN=192.168.201.3/24
# export IPv4GW=192.168.201.254
# export IPv6LAN=fc00:dead:beef:1201::3/64
# export IPv6GW=fc00:dead:beef:1201::ffff:ffff

export LXC_NAME=cl3-evpn2-202
export VLANLAN=202
export OVSLAN=pe13et0
export IPv4LAN=192.168.202.3/24
export IPv4GW=192.168.202.254
export IPv6LAN=fc00:dead:beef:1202::3/64
export IPv6GW=fc00:dead:beef:1202::ffff:ffff



echo "Creating VM ${LXC_NAME}"
lxc copy client ${LXC_NAME}
lxc query --request PATCH /1.0/instances/${LXC_NAME} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
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
    address ${IPv4LAN}
    gateway ${IPv4GW}
iface eth0 inet6 static
    address ${IPv6LAN}
    gateway ${IPv6GW}
EOF

lxc file push ./interface.conf ${LXC_NAME}/etc/network/interfaces
lxc start ${LXC_NAME}