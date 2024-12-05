### RR 
set interfaces lo0 unit 0 family inet6 address fc00:dead:beef:ffff::ffff:10/128
set interfaces lo0 unit 0 family iso address 49.0001.0101.0025.5010.00
set routing-options source-packet-routing srv6 locator SRV6-LOC-1 fc00:dead:beef:ff10::/64
set routing-options router-id 10.100.255.10
set protocols isis interface eth1 level 1 disable
set protocols isis interface eth1 point-to-point
set protocols isis interface lo0.0 level 1 disable
set protocols isis interface lo0.0 passive
set protocols isis source-packet-routing srv6 locator SRV6-LOC-1 end-sid fc00:dead:beef:ff10::
set protocols isis level 2 authentication-key "$9$H.fQ69A0BE9CK8LxsYTzF/9AtuO1Ec"
set protocols isis level 2 authentication-type md5

set routing-options autonomous-system 4200000001
set protocols bgp group to_int type internal
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:10
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int family evpn signaling advertise-srv6-service
set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int cluster 10.100.255.10
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:1
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:2
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:3




set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:4



set protocols bgp group to_int1 type internal
set protocols bgp group to_int1 local-address fc00:dead:beef:ffff::ffff:20
set protocols bgp group to_int1 family inet unicast extended-nexthop
set protocols bgp group to_int1 family inet unicast advertise-srv6-service
set protocols bgp group to_int1 family inet unicast accept-srv6-service
set protocols bgp group to_int1 cluster 10.100.255.10
set protocols bgp group to_int1 neighbor fc00:dead:beef:ffff::ffff:5


### PE1


set routing-options autonomous-system 4200000001
set protocols bgp group to_int type internal
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:1
set protocols bgp group to_int family evpn signaling advertise-srv6-service
set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:10
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy

set interface lo0 unit 1 family inet
set interface lo0 unit 1 family inet6
set routing-options route-distinguisher-id 10.100.255.1
set routing-instances VRF1 instance-type vrf
set routing-instances VRF1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances VRF1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances VRF1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances VRF1 interface ge-0/0/0.0
set routing-instances VRF1 interface lo0.1
set routing-instances VRF1 vrf-target target:65412:1001
set routing-instances VRF1 vrf-table-label
delete  protocols isis interface ge-0/0/0.0
set routing-instances VRF1 forwarding-options dhcp-relay forward-only
set routing-instances VRF1 forwarding-options dhcp-relay server-group dhcp-server 172.16.55.4
set routing-instances VRF1 forwarding-options dhcp-relay active-server-group dhcp-server
set routing-instances VRF1 forwarding-options dhcp-relay group dhcp interface ge-0/0/0.0


set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int family evpn signaling advertise-srv6-service
set policy-options policy-statement from_evpn term 1 from protocol evpn
set policy-options policy-statement from_evpn term 1 then accept






set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 172.16.11.0/24 orlonger
set policy-options policy-statement to_int term 1 from route-filter 10.100.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set protocols bgp group to_int export to_int

set system name-server 10.49.32.95
set system name-server 10.49.32.97
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service


### PE2


set routing-options autonomous-system 4200000001
set protocols bgp group to_int type internal
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:2
set protocols bgp group to_int family evpn signaling advertise-srv6-service
set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:10
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy
set routing-options route-distinguisher-id 10.100.255.2
set interface lo0 unit 1 family inet
set interface lo0 unit 1 family inet6
set routing-instances VRF1 instance-type vrf
set routing-instances VRF1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances VRF1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances VRF1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances VRF1 interface ge-0/0/0.0
set routing-instances VRF1 interface lo0.1
set routing-instances VRF1 vrf-target target:65412:1001
set routing-instances VRF1 vrf-table-label
delete  protocols isis interface ge-0/0/0.0
set routing-instances VRF1 forwarding-options dhcp-relay forward-only
set routing-instances VRF1 forwarding-options dhcp-relay server-group dhcp-server 172.16.55.4
set routing-instances VRF1 forwarding-options dhcp-relay active-server-group dhcp-server
set routing-instances VRF1 forwarding-options dhcp-relay group dhcp interface ge-0/0/0.0





set routing-options autonomous-system 4200000001
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 172.16.12.0/24 orlonger
set policy-options policy-statement to_int term 1 from route-filter 10.100.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:2
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:10
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy
set system name-server 10.49.32.95
set system name-server 10.49.32.97

### PE3


set routing-options autonomous-system 4200000001
set protocols bgp group to_int type internal
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:3
set protocols bgp group to_int family evpn signaling advertise-srv6-service
set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:10
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy

set routing-options route-distinguisher-id 192.168.255.213
set routing-instances VRF1 instance-type vrf
set routing-instances VRF1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances VRF1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances VRF1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances VRF1 interface ge-0/0/0.0
set routing-instances VRF1 vrf-target target:65412:1001
set routing-instances VRF1 vrf-table-label
delete  protocols isis interface ge-0/0/0.0


set routing-options autonomous-system 4200000001
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 172.16.13.0/24 orlonger
set policy-options policy-statement to_int term 1 from route-filter 10.100.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:3
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:10
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy
set system name-server 10.49.32.95
set system name-server 10.49.32.97


### PE4

set routing-options autonomous-system 4200000001
set protocols bgp group to_int type internal
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:4
set protocols bgp group to_int family evpn signaling advertise-srv6-service
set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:10
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy


set routing-options route-distinguisher-id 10.100.255.4
set interfaces lo0 unit 1 family inet
set interfaces lo0 unit 1 family inet6
set routing-instances VRF1 instance-type vrf
set routing-instances VRF1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances VRF1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances VRF1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances VRF1 interface ge-0/0/0.0
set routing-instances VRF1 interface lo0.1
set routing-instances VRF1 vrf-target target:65412:1001
set routing-instances VRF1 vrf-table-label
delete  protocols isis interface ge-0/0/0.0
set routing-instances VRF1 routing-options static route 172.16.55.0/24 next-hop 172.16.14.254



set routing-options autonomous-system 4200000001
set routing-option static route 172.16.55.0/24 next-hop 172.16.14.254
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 172.16.14.0/24 orlonger
set policy-options policy-statement to_int term 1 from route-filter 10.100.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set policy-options policy-statement to_int term 2 from protocol static
set policy-options policy-statement to_int term 2 then next-hop self
set policy-options policy-statement to_int term 2 then accept
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:4 
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:10
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy
set system name-server 10.49.32.95
set system name-server 10.49.32.97




vmm bind apstra && vmm bind apstraw2 && vmm bind apstraw3 && vmm bind ztp
vmm args apstra | grep mac
vmm args apstraw2 | grep mac
vmm args apstraw3 | grep mac
vmm args ztp | grep mac
vmm start apstra
vmm start apstraw2
vmm start apstraw3
vmm start ztp


## PE1
set interfaces ge-0/0/0 encapsulation ethernet-bridge
set interfaces ge-0/0/0 unit 0

set routing-instances EVPN1 instance-type mac-vrf
set routing-instances EVPN1 protocols evpn encapsulation srv6
set routing-instances EVPN1 protocols evpn source-packet-routing srv6 locator SRV6-LOC-1
set routing-instances EVPN1 protocols evpn source-packet-routing srv6 locator end-dt2-sid
set routing-instances EVPN1 bridge-domains bd10 domain-type bridge
set routing-instances EVPN1 bridge-domains bd10 vlan-id 1
set routing-instances EVPN1 bridge-domains bd10 interface ge-0/0/0.0
set routing-instances EVPN1 service-type vlan-based
set routing-instances EVPN1 interface ge-0/0/0.0
set routing-instances EVPN1 vrf-target target:65412:1002