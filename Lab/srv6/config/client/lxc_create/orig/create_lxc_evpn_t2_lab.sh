#!/bin/bash
for i in c{1..4}evpn1
do
    echo "creating LXC ${i}"
    lxc copy client ${i}
done

# changing LXC container configuration, node router
VLAN=103
for i in {1..4}
do
echo "changing container c${i}evpn1"
if [ $i -eq 1 -o $i -eq 2 ];
then 
    OVS=ovs1
else
    OVS=ovs2
fi
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
done

# Changing lxc container configuration, node client

for i in {1..4}
do
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

for i in c{1..4}evpn1
do
    lxc start $i
done