## IP routing over SRv6

### PE11


set routing-options autonomous-system 4200000001
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 10.100.11.0/24 orlonger
set policy-options policy-statement to_int term 1 from route-filter 192.168.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:11
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:20
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy
set system name-server 10.49.32.95
set system name-server 10.49.32.97

set services rpm twamp server authentication-mode none
set services rpm twamp server client-list l1 address 172.16.211.10/32
set services rpm twamp server client-list l1 address 172.16.13.2/32
set services rpm twamp server client-list l1 address 172.16.13.10/32



delete interface ge-0/0/0 unit 0
set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 192.168.255.1/31
set interfaces ge-0/0/0 unit 101 family inet6 address fc00:dead:beef:ffff::1/127
set protocols bgp group to_ce neighbor 192.168.255.0 peer-as 4200001001
set protocols bgp group to_ce neighbor fc00:dead:beef:ffff:: peer-as 4200001001

### PE12



set routing-options autonomous-system 4200000001
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 10.100.12.0/24 orlonger
set policy-options policy-statement to_int term 1 from route-filter 192.168.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:12
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:20
set routing-options resolution preserve-nexthop-hierarchy
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set system name-server 10.49.32.95
set system name-server 10.49.32.97


delete interface ge-0/0/0 unit 0
set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 192.168.255.3/31
set interfaces ge-0/0/0 unit 101 family inet6 address fc00:dead:beef:ffff::3/127
set protocols bgp group to_ce neighbor 192.168.255.2 peer-as 4200001002
set protocols bgp group to_ce neighbor fc00:dead:beef:ffff::2 peer-as 4200001002



### PE13

set routing-options autonomous-system 4200000001
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 10.100.13.0/24 orlonger
set policy-options policy-statement to_int term 1 from route-filter 192.168.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:13
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:20
set routing-options resolution preserve-nexthop-hierarchy
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set system name-server 10.49.32.95
set system name-server 10.49.32.97


delete interface ge-0/0/0 unit 0
set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 192.168.255.5/31
set interfaces ge-0/0/0 unit 101 family inet6 address fc00:dead:beef:ffff::5/127

set protocols bgp group to_ce neighbor 192.168.255.4 peer-as 4200001003
set protocols bgp group to_ce neighbor fc00:dead:beef:ffff::4 peer-as 4200001003

### PE14


set routing-options autonomous-system 4200000001
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 10.100.14.0/24 orlonger
set policy-options policy-statement to_int term 1 from route-filter 192.168.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:14
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:20
set routing-options resolution preserve-nexthop-hierarchy
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set system name-server 10.49.32.95
set system name-server 10.49.32.97

delete interface ge-0/0/0 unit 0
set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 192.168.255.7/31
set interfaces ge-0/0/0 unit 101 family inet6 address fc00:dead:beef:ffff::7/127
set protocols bgp group to_ce neighbor 192.168.255.6 peer-as 4200001004
set protocols bgp group to_ce neighbor fc00:dead:beef:ffff::6 peer-as 4200001004


### PE15
set system name-server 10.49.32.95
set system name-server 10.49.32.97
set routing-options autonomous-system 4200000001
set routing-options static route 0.0.0.0/0 next-hop 172.16.11.254
set policy-options policy-statement to_int term 1 from protocol static
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 0.0.0.0/0 exact
set policy-options policy-statement to_int term 1 from route-filter 192.168.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set policy-options policy-statement to_int term default then reject
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:15
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:20
set routing-options resolution preserve-nexthop-hierarchy
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop



set policy-options policy-statement from_static term 1 from protocol static
set policy-options policy-statement from_static term 1 from route-filter fc00:dead:beef:bb12::/64 orlonger
set policy-options policy-statement from_static term 1 from route-filter fc00:dead:beef:bb13::/64 orlonger
set policy-options policy-statement from_static term 1 then accept
set routing-options rib inet6.0 static route fc00:dead:beef:bb12::/64 next-hop fc00:dead:beef:aa15::1000:ffff
set routing-options rib inet6.0 static route fc00:dead:beef:bb13::/64 next-hop fc00:dead:beef:aa15::1000:ffff
set protocols isis export from_static




### RR 
set interfaces lo0 unit 0 family inet6 address fc00:dead:beef:ffff::ffff:20/128
set interfaces lo0 unit 0 family iso address 49.0001.1921.6800.0020.00
set routing-options source-packet-routing srv6 locator SRV6-LOC-1 fc00:dead:beef:ff20::/64
set routing-options router-id 192.168.255.200
set protocols isis interface eth1 level 1 disable
set protocols isis interface eth1 point-to-point
set protocols isis interface lo0.0 level 1 disable
set protocols isis interface lo0.0 passive
set protocols isis source-packet-routing srv6 locator SRV6-LOC-1 end-sid fc00:dead:beef:ff20::
set protocols isis level 2 authentication-key "$9$H.fQ69A0BE9CK8LxsYTzF/9AtuO1Ec"
set protocols isis level 2 authentication-type md5

set routing-options autonomous-system 4200000001
set protocols bgp group to_int type internal
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:20
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int family evpn signaling advertise-srv6-service
set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int cluster 192.168.255.200
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:11
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:14
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:12
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:13
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:15


set protocols bgp group to_int1 type internal
set protocols bgp group to_int1 local-address fc00:dead:beef:ffff::ffff:20
set protocols bgp group to_int1 family inet unicast extended-nexthop
set protocols bgp group to_int1 family inet unicast advertise-srv6-service
set protocols bgp group to_int1 family inet unicast accept-srv6-service
set protocols bgp group to_int1 cluster 192.168.255.200
set protocols bgp group to_int1 neighbor fc00:dead:beef:ffff::ffff:1
set protocols bgp group to_int1 neighbor fc00:dead:beef:ffff::ffff:2
set protocols bgp group to_int1 neighbor fc00:dead:beef:ffff::ffff:3
set protocols bgp group to_int1 neighbor fc00:dead:beef:ffff::ffff:4
set protocols bgp group to_int1 neighbor fc00:dead:beef:ffff::ffff:5

set protocols bgp group to_int1 export to_int
set policy-options policy-statement to_int term 1 from route-filter 0.0.0.0/0 exact
set policy-options policy-statement to_int term 1 then accept
set policy-options policy-statement to_int term 2 from route-filter 192.168.255.0/24 orlonger
set policy-options policy-statement to_int term 2 then accept
set policy-options policy-statement to_int term default then reject

### P1
set system name-server 10.49.32.95
set system name-server 10.49.32.97
set routing-options autonomous-system 4200000001
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 192.168.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:1
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:20
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy



set policy-options policy-statement to_int term 2 from protocol static
set policy-options policy-statement to_int term 2 from route-filter 0.0.0.0/0 exact

set policy-options policy-statement to_int term 9999 then next-hop self
set policy-options policy-statement to_int term 9999 then accept


### P2
set system name-server 10.49.32.95
set system name-server 10.49.32.97
set routing-options autonomous-system 4200000001
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 192.168.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set policy-options policy-statement to_int term default then reject
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:2
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:20
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy


set policy-options policy-statement to_int term 2 from protocol static
set policy-options policy-statement to_int term 2 from route-filter 0.0.0.0/0 exact

### P3
set system name-server 10.49.32.95
set system name-server 10.49.32.97
set routing-options autonomous-system 4200000001
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 192.168.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set policy-options policy-statement to_int term default then reject
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:3
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:20
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy


set policy-options policy-statement to_int term 2 from protocol static
set policy-options policy-statement to_int term 2 from route-filter 0.0.0.0/0 exact

### P4
set system name-server 10.49.32.95
set system name-server 10.49.32.97
set routing-options autonomous-system 4200000001
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 192.168.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set policy-options policy-statement to_int term default then reject
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:4
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:20
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy

set policy-options policy-statement to_int term 2 from protocol static
set policy-options policy-statement to_int term 1 from route-filter 0.0.0.0/0 exact


### P5
set system name-server 10.49.32.95
set system name-server 10.49.32.97
set routing-options autonomous-system 4200000001
set policy-options policy-statement to_int term 1 from protocol direct
set policy-options policy-statement to_int term 1 from route-filter 192.168.255.0/24 prefix-length-range /32-/32
set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept
set policy-options policy-statement to_int term default then reject
set protocols bgp group to_int type internal
set protocols bgp group to_int export to_int
set protocols bgp group to_int local-address fc00:dead:beef:ffff::ffff:5
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int neighbor fc00:dead:beef:ffff::ffff:20
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop
set routing-options resolution preserve-nexthop-hierarchy


set policy-options policy-statement to_int term 2 from protocol static
set policy-options policy-statement to_int term 2 from route-filter 0.0.0.0/0 exact

## EVPN type 5 over SRv6

### PE11

set routing-options route-distinguisher-id 192.168.255.211
set interfaces ge-0/0/0 unit 102 vlan-id 102
set interfaces ge-0/0/0 unit 102 family inet address 192.168.255.9/31
set interfaces ge-0/0/0 unit 102 family inet6 address fc00:dead:beef:ffff::9/127

set policy-options policy-statement from_evpn term 1 from protocol evpn
set policy-options policy-statement from_evpn term 1 then accept

set routing-instances VRF1 instance-type vrf
set routing-instances VRF1 protocols bgp group to_ce export from_evpn
set routing-instances VRF1 protocols bgp group to_ce neighbor 192.168.255.8 peer-as  4200001011
set routing-instances VRF1 protocols bgp group to_ce neighbor fc00:dead:beef:ffff::8 family inet6 any
set routing-instances VRF1 protocols bgp group to_ce neighbor fc00:dead:beef:ffff::8 peer-as 4200001011
set routing-instances VRF1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances VRF1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances VRF1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances VRF1 interface ge-0/0/0.102
set routing-instances VRF1 vrf-target target:65412:1001

set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int family evpn signaling advertise-srv6-service
set routing-instances VRF1 vrf-table-label


### PE12

set routing-options route-distinguisher-id 192.168.255.212
set interfaces ge-0/0/0 unit 102 vlan-id 102
set interfaces ge-0/0/0 unit 102 family inet address 192.168.255.11/31
set interfaces ge-0/0/0 unit 102 family inet6 address fc00:dead:beef:ffff::11/127

set policy-options policy-statement from_evpn term 1 from protocol evpn
set policy-options policy-statement from_evpn term 1 then accept

set routing-instances VRF1 instance-type vrf
set routing-instances VRF1 protocols bgp group to_ce export from_evpn
set routing-instances VRF1 protocols bgp group to_ce neighbor 192.168.255.10 peer-as  4200001012
set routing-instances VRF1 protocols bgp group to_ce neighbor fc00:dead:beef:ffff::10 family inet6 any
set routing-instances VRF1 protocols bgp group to_ce neighbor fc00:dead:beef:ffff::10 peer-as 4200001012
set routing-instances VRF1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances VRF1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances VRF1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances VRF1 interface ge-0/0/0.102
set routing-instances VRF1 vrf-target target:65412:1001

set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int family evpn signaling advertise-srv6-service
set routing-instances VRF1 vrf-table-label



### PE13

set routing-options route-distinguisher-id 192.168.255.213
set interfaces ge-0/0/0 unit 102 vlan-id 102
set interfaces ge-0/0/0 unit 102 family inet address 192.168.255.13/31
set interfaces ge-0/0/0 unit 102 family inet6 address fc00:dead:beef:ffff::13/127

set policy-options policy-statement from_evpn term 1 from protocol evpn
set policy-options policy-statement from_evpn term 1 then accept

set routing-instances VRF1 instance-type vrf
set routing-instances VRF1 protocols bgp group to_ce export from_evpn
set routing-instances VRF1 protocols bgp group to_ce neighbor 192.168.255.12 peer-as  4200001013
set routing-instances VRF1 protocols bgp group to_ce neighbor fc00:dead:beef:ffff::12 family inet6 any
set routing-instances VRF1 protocols bgp group to_ce neighbor fc00:dead:beef:ffff::12 peer-as 4200001013
set routing-instances VRF1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances VRF1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances VRF1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances VRF1 interface ge-0/0/0.102
set routing-instances VRF1 vrf-target target:65412:1001

set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int family evpn signaling advertise-srv6-service


set routing-instances VRF1 vrf-table-label


### PE14

set routing-options route-distinguisher-id 192.168.255.214
set interfaces ge-0/0/0 unit 102 vlan-id 102
set interfaces ge-0/0/0 unit 102 family inet address 192.168.255.15/31
set interfaces ge-0/0/0 unit 102 family inet6 address fc00:dead:beef:ffff::15/127

set policy-options policy-statement from_evpn term 1 from protocol evpn
set policy-options policy-statement from_evpn term 1 then accept

set routing-instances VRF1 instance-type vrf
set routing-instances VRF1 protocols bgp group to_ce export from_evpn
set routing-instances VRF1 protocols bgp group to_ce neighbor 192.168.255.14 peer-as  4200001014
set routing-instances VRF1 protocols bgp group to_ce neighbor fc00:dead:beef:ffff::14 family inet6 any
set routing-instances VRF1 protocols bgp group to_ce neighbor fc00:dead:beef:ffff::14 peer-as 4200001014
set routing-instances VRF1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances VRF1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances VRF1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances VRF1 interface ge-0/0/0.102
set routing-instances VRF1 vrf-target target:65412:1001

set protocols bgp group to_int family evpn signaling accept-srv6-service
set protocols bgp group to_int family evpn signaling advertise-srv6-service


set routing-instances VRF1 vrf-table-label


## EVPN type 2 over SRv6

### PE11/PE12/PE13/PE14

set interfaces ge-0/0/0 unit 103 vlan-id 103
set interfaces ge-0/0/0 unit 103 encapsulation vlan-bridge
set interfaces ge-0/0/0 unit 103 vlan-id 103

set routing-instances EVPN1 instance-type mac-vrf
set routing-instances EVPN1 protocols evpn encapsulation srv6
set routing-instances EVPN1 protocols evpn source-packet-routing srv6 locator SRV6-LOC-1
set routing-instances EVPN1 protocols evpn source-packet-routing srv6 locator end-dt2-sid
set routing-instances EVPN1 bridge-domains bd10 domain-type bridge
set routing-instances EVPN1 bridge-domains bd10 vlan-id 103
set routing-instances EVPN1 bridge-domains bd10 interface ge-0/0/0.103
set routing-instances EVPN1 service-type vlan-based
set routing-instances EVPN1 interface ge-0/0/0.103
set routing-instances EVPN1 vrf-target target:65412:1002


## EVPN-VPWS ver SRv6

### PE11
set interfaces ge-0/0/0 unit 111 encapsulation vlan-ccc
set interfaces ge-0/0/0 unit 111 vlan-id 111
set interfaces ge-0/0/0 unit 112 encapsulation vlan-ccc
set interfaces ge-0/0/0 unit 112 vlan-id 112
set interfaces ge-0/0/0 unit 113 encapsulation vlan-ccc
set interfaces ge-0/0/0 unit 113 vlan-id 113
set routing-instances EVPN2 instance-type evpn-vpws
set routing-instances EVPN2 interface ge-0/0/0.111
set routing-instances EVPN2 interface ge-0/0/0.112
set routing-instances EVPN2 interface ge-0/0/0.113
set routing-instances EVPN2 protocols evpn encapsulation srv6
set routing-instances EVPN2 vrf-target target:65412:2001
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.111 vpws-service-id local 1
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.111 vpws-service-id remote 1
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.111 vpws-service-id source-packet-routing srv6 locator SRV6-LOC-1
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.112 vpws-service-id local 2
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.112 vpws-service-id remote 2
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.112 vpws-service-id source-packet-routing srv6 locator SRV6-LOC-1
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.113 vpws-service-id local 3
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.113 vpws-service-id remote 3
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.113 vpws-service-id source-packet-routing srv6 locator SRV6-LOC-1


### PE12
set interfaces ge-0/0/0 unit 111 encapsulation vlan-ccc
set interfaces ge-0/0/0 unit 111 vlan-id 111
set routing-instances EVPN2 instance-type evpn-vpws
set routing-instances EVPN2 interface ge-0/0/0.111
set routing-instances EVPN2 protocols evpn encapsulation srv6
set routing-instances EVPN2 vrf-target target:65412:2001
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.111 vpws-service-id local 1
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.111 vpws-service-id remote 1
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.111 vpws-service-id source-packet-routing srv6 locator SRV6-LOC-1


### PE13
set interfaces ge-0/0/0 unit 112 encapsulation vlan-ccc
set interfaces ge-0/0/0 unit 112 vlan-id 112
set routing-instances EVPN2 instance-type evpn-vpws
set routing-instances EVPN2 interface ge-0/0/0.112
set routing-instances EVPN2 protocols evpn encapsulation srv6
set routing-instances EVPN2 vrf-target target:65412:2001
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.112 vpws-service-id local 2
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.112 vpws-service-id remote 2
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.112 vpws-service-id source-packet-routing srv6 locator SRV6-LOC-1


### PE14
set interfaces ge-0/0/0 unit 113 encapsulation vlan-ccc
set interfaces ge-0/0/0 unit 113 vlan-id 113
set routing-instances EVPN2 instance-type evpn-vpws
set routing-instances EVPN2 interface ge-0/0/0.113
set routing-instances EVPN2 protocols evpn encapsulation srv6
set routing-instances EVPN2 vrf-target target:65412:2001
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.113 vpws-service-id local 3
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.113 vpws-service-id remote 3
set routing-instances EVPN2 protocols evpn interface ge-0/0/0.113 vpws-service-id source-packet-routing srv6 locator SRV6-LOC-1

