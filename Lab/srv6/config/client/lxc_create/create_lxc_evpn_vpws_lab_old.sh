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

for i in {3..4}
do

if [ $i -eq 3 ];
then
    EP=1
    RP=0
    NET=101
    ASME=3001
    ASYOU=3002
else
    EP=0
    RP=1
    NET=102
    ASME=3002
    ASYOU=3001
fi
cat << EOF | tee interfaces
auto eth0
iface eth0 inet static
    address 192.168.255.${RP}/31
    mtu 1500
auto eth1
iface eth1 inet static
    address 192.168.${NET}.1/24
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:ffff::${RP}/127
iface eth1 inet6 static
    address fc00:dead:beef:a${NET}::1/64
EOF

cat << EOF | tee frr.conf 
frr defaults traditional
hostname ce${i}
log syslog informational
service integrated-vtysh-config
ipv6 forwarding
!
router bgp 420000${ASME}
 no bgp ebgp-requires-policy
 neighbor 192.168.255.${EP} remote-as 420000${ASYOU}
 neighbor fc00:dead:beef:ffff::${EP} remote-as 420000${ASYOU}
 !
 address-family ipv4 unicast
  network 192.168.${NET}.0/24
 exit-address-family
 !
 address-family ipv6 unicast
  network fc00:dead:beef:a${NET}::/64
  neighbor fc00:dead:beef:ffff::${EP}  activate
 exit-address-family
exit
!
EOF

cat << EOF | tee dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
log-facility local7;
subnet 192.168.${NET}.0 netmask 255.255.255.0 {
  range 192.168.${NET}.101 192.168.${NET}.200;
  option routers 192.168.${NET}.1;
}
EOF

cat << EOF | tee radvd.conf
interface eth1
{
    AdvSendAdvert on;
    prefix fc00:dead:beef:a${NET}::0/64
    {
        AdvOnLink on;
        AdvAutonomous on;
        AdvRouterAddr on;
    };
};
EOF

    echo "push configuration into node ce${i}"
    lxc file push interfaces ce${i}/etc/network/interfaces
    lxc file push frr.conf ce${i}/etc/frr/frr.conf
    lxc file push dhcpd.conf ce${i}/etc/dhcp/dhcpd.conf
    lxc file push radvd.conf ce${i}/etc/radvd.conf
done

for i in ce{3..4} 
do
    lxc start $i
    for j in c{1..2}
    do
        lxc start ${j}${i}
    done
done