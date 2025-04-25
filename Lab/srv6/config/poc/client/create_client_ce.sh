#!/bin/bash
export LXC_NAME=c2pe12
export VLAN=51
export OVS=global_pe12
export IPv4=192.168.212.12/24
export GWv4=192.168.212.1
export IPv6=fc00:dead:beef:b212::1000:12/64
export GWv6=fc00:dead:beef:b212::1


echo "Creating VM ${LXC_NAME}"
lxc copy client ${LXC_NAME}
lxc query --request PATCH /1.0/instances/${LXC_NAME} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${OVS}\",
       \"type\": \"nic\"
    }
  }
}"
echo "push configuration into node ${LXC_NAME}"
cat << EOF | tee ./interface.conf
auto eth0
iface eth0 inet static
    address ${IPv4}
    mtu 1500
    gateway ${GWv4}
iface eth0 inet6 static
    address ${IPv6}
    gateway ${GWv6}
EOF

lxc file push ./interface.conf ${LXC_NAME}/etc/network/interfaces
cat << EOF | tee ./resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF
lxc file push ./resolv.conf ${LXC_NAME}/etc/resolv.conf

lxc start ${LXC_NAME}
