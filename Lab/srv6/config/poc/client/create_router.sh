#!/bin/bash
export LXC_NAME=cepe12
export VLAN=51
export OVS=pe12ge0
export CLIENTBR=global_pe12
export IPv4e0=172.16.11.5/31 
export IPv6e0=fc00:dead:beef:b011::5/127
export IPv4e1=192.168.212.1/24
export IPv6e1=fc00:dead:beef:b212::1/64

echo "Creating VM ${LXC_NAME}"
lxc copy router ${LXC_NAME}
lxc query --request PATCH /1.0/instances/${LXC_NAME} --data "{
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
       \"parent\": \"${CLIENTBR}\",
       \"type\": \"nic\"
    }
  }
}"
echo "push configuration into node ${LXC_NAME}"
cat << EOF | tee ./interface.conf
auto eth0
iface eth0 inet static
    address ${IPv4e0}
    mtu 1500
iface eth0 inet6 static
    address ${IPv6e0}
auto eth1
iface eth1 inet static
    address ${IPv4e1}
    mtu 1500
iface eth1 inet6 static
    address ${IPv6e1}
EOF

lxc file push ./interface.conf ${LXC_NAME}/etc/network/interfaces
cat << EOF | tee ./resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF
lxc file push ./resolv.conf ${LXC_NAME}/etc/resolv.conf

lxc start ${LXC_NAME}
