#!/bin/bash
for i in ce{3..4}
do 
    echo "creating LXC ${i}"
    lxc copy router ${i}
done 

for i in ce{3..4}
do
    for j in c{1..2}
    do
        echo "creating LXC ${j}${i}"
        lxc copy client ${j}${i}
    done
done

# changing LXC container configuration, node router
VLAN=102
for i in {3..4}
do
echo "changing container ce${i}"
if (( $i == 3 ));
then 
    OVS=ovs1
else
    OVS=ovs2
fi
lxc query --request PATCH /1.0/instances/ce${i} --data "{
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
       \"parent\": \"ce${i}eth1\",
       \"type\": \"nic\"
    }
  }
}"
done

# Changing lxc container configuration, node client

for i in ce{3..4}
do 
    for j in c{1..2}
    do
        echo "changing container ${j}${i}"
        lxc query --request PATCH /1.0/instances/${j}${i} --data "{
        \"devices\": {
                \"eth0\" : {
                    \"name\": \"eth0\",
                    \"nictype\": \"bridged\",
                    \"parent\": \"${i}eth1\",
                    \"type\": \"nic\"
                }
            }
        }"
    done
done

for i in ce{3..4}
do
    echo "push configuration into node ${i}"
    lxc file push ${i}/interfaces ${i}/etc/network/interfaces
    lxc file push ${i}/frr.conf ${i}/etc/frr/frr.conf
    lxc file push ${i}/dhcpd.conf ${i}/etc/dhcp/dhcpd.conf
    lxc file push ${i}/radvd.conf ${i}/etc/radvd.conf
done

for i in ce{3..4} 
do
    lxc start $i
    for j in c{1..2}
    do
        lxc start ${j}${i}
    done
done