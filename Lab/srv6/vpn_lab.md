### PE11

set routing-options route-distinguisher-id 192.168.255.211
set interfaces ge-0/0/0 unit 111 vlan-id 111
set interfaces ge-0/0/0 unit 111 family inet address 172.16.111.1/24
set interfaces ge-0/0/0 unit 111 family inet6 address fc00:dead:beef:aa11::1/64

set policy-options policy-statement from_evpn term 1 from protocol evpn
set policy-options policy-statement from_evpn term 1 then accept

set routing-instances VRF1 instance-type vrf
set routing-instances VRF1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances VRF1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances VRF1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances VRF1 interface ge-0/0/0.111
set routing-instances VRF1 vrf-target target:65412:1111
set routing-instances VRF1 vrf-table-label

set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int family evpn signaling advertise-srv6-service




set interfaces ge-0/0/5 unit 0 family inet address 172.16.121.1/24
set interfaces ge-0/0/5 unit 0 family inet6 address fc00:dead:beef:aa12::1/64
set routing-instances VRF1 interface ge-0/0/5.0



CLIENT=c1pe11
BR=pe11ge0
VLAN=111
echo "changing container ${CLIENT}"
lxc copy client ${CLIENT}
lxc query --request PATCH /1.0/instances/${CLIENT} --data "{
\"devices\": {
        \"eth0\" : {
            \"name\": \"eth0\",
            \"nictype\": \"bridged\",
            \"parent\": \"${BR}\",
            \"vlan\" : \"${VLAN}\",
            \"type\": \"nic\"
        }
    }
}"
done

echo "changing container ${CLIENT}"
cat << EOF | tee interfaces
auto eth0
iface eth0 inet static
    address 172.16.111.10/24
    gateway 172.16.111.1
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:aa11::1000:10/64
    gateway fc00:dead:beef:aa11::1
EOF

echo "push configuration into node ${CLIENT}"
lxc file push interfaces ${CLIENT}/etc/network/interfaces
lxc start ${CLIENT}


### PE13

set routing-options route-distinguisher-id 192.168.255.213
set interfaces ge-0/0/0 unit 111 vlan-id 111
set interfaces ge-0/0/0 unit 111 family inet address 172.16.113.1/24
set interfaces ge-0/0/0 unit 111 family inet6 address fc00:dead:beef:aa13::1/64

set policy-options policy-statement from_evpn term 1 from protocol evpn
set policy-options policy-statement from_evpn term 1 then accept

set routing-instances VRF1 instance-type vrf
set routing-instances VRF1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances VRF1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances VRF1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances VRF1 interface ge-0/0/0.113
set routing-instances VRF1 vrf-target target:65412:1111
set routing-instances VRF1 vrf-table-label

set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int family evpn signaling advertise-srv6-service


set interfaces ge-0/0/5 unit 0 family inet address 172.16.123.1/24
set interfaces ge-0/0/5 unit 0 family inet6 address fc00:dead:beef:aa14::1/64
set routing-instances VRF1 interface ge-0/0/5.0


CLIENT=c1pe13
BR=pe13ge0
VLAN=111
echo "changing container ${CLIENT}"
lxc copy client ${CLIENT}
lxc query --request PATCH /1.0/instances/${CLIENT} --data "{
\"devices\": {
        \"eth0\" : {
            \"name\": \"eth0\",
            \"nictype\": \"bridged\",
            \"parent\": \"${BR}\",
            \"vlan\" : \"${VLAN}\",
            \"type\": \"nic\"
        }
    }
}"
done

echo "changing container ${CLIENT}"
cat << EOF | tee interfaces
auto eth0
iface eth0 inet static
    address 172.16.113.10/24
    gateway 172.16.113.1
    mtu 1500
iface eth0 inet6 static
    address fc00:dead:beef:aa13::1000:10/64
    gateway fc00:dead:beef:aa13::1
EOF

echo "push configuration into node ${CLIENT}"
lxc file push interfaces ${CLIENT}/etc/network/interfaces
lxc start ${CLIENT}

