# Start LXC instance
lxc launch alpine --name lxc

export LXC_NAME=cl2pe1
export VLAN=101
export OVS=pe1ovs
export IPv4=10.200.101.12/24
export GWv4=10.200.101.1
export IPv6=fc00:dead:beef:a101::1000:12/64
export GWv6=fc00:dead:beef:a101::1


echo "Creating VM ${LXC_NAME}"
lxc copy client ${LXC_NAME}
lxc query --request PATCH /1.0/instances/${LXC_NAME} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${OVS}\",
       \"vlan\" : \"${VLAN}\",
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
EOF

lxc file push ./interface.conf ${LXC_NAME}/etc/network/interfaces
cat << EOF | tee ./resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF
lxc file push ./resolv.conf ${LXC_NAME}/etc/resolv.conf



export LXC_NAME=cl2pe2
export VLAN=102
export OVS=pe2ovs
export IPv4=10.200.102.12/24
export GWv4=10.200.102.1
export IPv6=fc00:dead:beef:a102::1000:12/64
export GWv6=fc00:dead:beef:a102::1


echo "Creating VM ${LXC_NAME}"
lxc copy client ${LXC_NAME}
lxc query --request PATCH /1.0/instances/${LXC_NAME} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${OVS}\",
       \"vlan\" : \"${VLAN}\",
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
EOF

lxc file push ./interface.conf ${LXC_NAME}/etc/network/interfaces
cat << EOF | tee ./resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF
lxc file push ./resolv.conf ${LXC_NAME}/etc/resolv.conf