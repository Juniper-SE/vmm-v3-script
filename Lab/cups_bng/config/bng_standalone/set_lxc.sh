export LXC_NAME=client1
#export VLAN=12
export OVS=cpe1c
export IPv4=172.16.15.5/24
export GWv4=172.16.15.1
export IPv6=fc00:dead:beef:fe15::1000:2/64
export GWv6=fc00:dead:beef:fe15::1


echo "Creating VM ${LXC_NAME}"
lxc copy alpine ${LXC_NAME}
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
nameserver 172.16.15.5
search vmmlab.com
EOF
lxc file push ./resolv.conf ${LXC_NAME}/etc/resolv.conf
lxc start ${LXC_NAME}



cat << EOF | sudo tee /etc/netplan/01_net.yaml
network:
  ethernets:
    eth0:
      dhcp4: false
    eth1:
      dhcp4: false
    eth2:
      dhcp4: false
    eth3:
      dhcp4: false
    eth4:
      dhcp4: false
    eth5:
      dhcp4: false
  bridges:
    cpnet:
      interfaces:
      - eth0
      addresses : ['172.16.11.114/24']
      nameservers:
         addresses: ['10.49.32.95', '10.49.32.97']
      routes:
       - to: 0.0.0.0/0
         via: 172.16.11.1
         metric: 1
    cpe1c:
      interfaces:
      - eth1
    cpe2c:
      interfaces:
      - eth2
    cpe3c:
      interfaces:
      - eth3
    cpe4c:
      interfaces:
      - eth4
    net5:
      interfaces:
      - eth5
EOF

