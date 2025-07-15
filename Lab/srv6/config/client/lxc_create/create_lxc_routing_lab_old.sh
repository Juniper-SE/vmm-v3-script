#!/bin/bash
for i in ce{1..2}
do 
    echo "creating LXC ${i}"
    lxc copy router ${i}
done 

for i in ce{1..2}
do
    for j in c{1..2}
    do
        echo "creating LXC ${j}${i}"
        lxc copy client ${j}${i}
    done
done

# changing LXC container configuration, node router
for i in {1..2}
do
echo "changing container ce${i}"
lxc query --request PATCH /1.0/instances/ce${i} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"ovs${i}\",
       \"vlan\" : \"101\",
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

for i in ce{1..2}
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

for i in {1..2}
do
if [ $i -eq 1 ];
then
    EP=1
    RP=0
else
    EP=3
    RP=2
fi
cat << EOF | tee interfaces
auto eth0
iface eth0 inet static
    address 200.200.1.${EP}/31
    mtu 1500
iface eth0 inet6 static
    address 2001:dead:beef:2001::${EP}/127
auto eth1
iface eth1 inet static
    address 200.200.10${i}.1/24
    mtu 1500
iface eth1 inet6 static
    address 2001:dead:beef:a10${i}::1/64
EOF

cat << EOF | tee frr.conf 
frr defaults traditional
hostname ce${i}
log syslog informational
service integrated-vtysh-config
ipv6 forwarding
!
router bgp 420000100${i}
 no bgp ebgp-requires-policy
 neighbor 200.200.1.${RP} remote-as 4200000001
 neighbor 2001:dead:beef:2001::${RP} remote-as 4200000001
 !
 address-family ipv4 unicast
  network 200.200.10${i}.0/24
 exit-address-family
 !
 address-family ipv6 unicast
  network 2001:dead:beef:a10${i}::/64
  neighbor 2001:dead:beef:2001::${RP} activate
 exit-address-family
exit
!
EOF

cat << EOF | tee dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
log-facility local7;
subnet 200.200.10${i}.0 netmask 255.255.255.0 {
  range 200.200.10${i}.101 200.200.10${i}.102;
  option routers 200.200.10${i}.1;
}
EOF

cat << EOF | tee radvd.conf
interface eth1
{
     AdvSendAdvert on;
    prefix 2001:dead:beef:a10${i}::/64
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

for i in ce{1..2} 
do
    lxc start $i
    for j in c{1..2}
    do
        lxc start ${j}${i}
    done
done