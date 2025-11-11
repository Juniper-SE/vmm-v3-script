#!/bin/bash
# create router container
YOURIP=8
MYIP=`expr ${YOURIP} + 1`
for i in {1..4}
do
for j in {1..2}
do
VLAN=10${i}
LXC=c${i}${j}
NODE=r${i}
# if [ "${NODE}" = "r3" ];
# then
#   INTF="et0"
# else
#   INTF="ge0"
# fi
# INTF="ge0"
# OVS=${NODE}_${INTF}
OVS=${NODE}
echo "create client ${LXC} "
lxc copy client ${LXC}
echo "changing container ${LXC}"
lxc query --request PATCH /1.0/instances/${LXC} --data "{
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

echo "changing containers${LXC}"
cat << EOF | tee interfaces
auto eth0
iface eth0 inet static
    address 192.168.${i}0.${j}/24
    gateway 192.168.${i}0.254
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:aa${i}0::1000:${j}/64
    gateway fc00:dead:beef:aa${i}0::1
EOF


echo "push configuration into node ${LXC}"
lxc file push interfaces  ${LXC}/etc/network/interfaces
lxc start ${LXC}

done
done