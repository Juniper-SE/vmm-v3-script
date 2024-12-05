#!/bin/bash
for i in {1..4} 
do
    echo "creating LXC c${i}evpn1"
    lxc copy client c${i}evpn1
# changing LXC container configuration, node router
VLAN=103
OVS=ovs${i}
echo "changing container c${i}evpn1"
lxc query --request PATCH /1.0/instances/c${i}evpn1 --data "{
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
# Changing lxc container configuration, node client
echo "push configuration into node c${i}evpn1"
cat << EOF | tee ./interface.conf
auto eth0
iface eth0 inet static
    address 192.168.10.${i}/24
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:aa10::${i}/64
EOF

lxc file push ./interface.conf c${i}evpn1/etc/network/interfaces
done

lxc start c{1..4}evpn1