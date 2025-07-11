# configure network
cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  ethernets:
    eth1:
      dhcp4: false
      mtu: 9000
    eth2:
      dhcp4: false
      mtu: 9000
  bridges:
    pe1ge0:
      openvswitch: {}
      interfaces:
      - eth1
    pe2ge0:
      openvswitch: {}
      interfaces:
      - eth2
EOF
    

# Start LXC instance
lxc image copy images:alpine/edge local: --alias alpine

lxc launch alpine client

export LXC_NAME=cl1pe2
export VLAN=102
export OVS=pe2ge0
export IPv4=10.200.102.11/24
export GWv4=110.200.102.1
export IPv6=fc00:dead:beef:a102::1000:11/64
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
    gateway ${GWv6}
EOF

lxc file push ./interface.conf ${LXC_NAME}/etc/network/interfaces
cat << EOF | tee ./resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF
lxc file push ./resolv.conf ${LXC_NAME}/etc/resolv.conf
lxc start  ${LXC_NAME}