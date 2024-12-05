# Configuring BGP free core using SRv6

## configuration for PE11


set routing-options resolution preserve-nexthop-hierarchy
set routing-options router-id 192.168.0.11
set routing-options autonomous-system 4200000001

set protocols bgp group to_int type internal
set protocols bgp group to_int local-address bad:cafe::11
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int export to_int
set protocols bgp group to_int neighbor bad:cafe::12
set protocols bgp group to_ce1 neighbor 200.200.1.1 peer-as 4200001001
set protocols bgp group to_ce1 neighbor 2001:dead:beef:2001::1 peer-as 4200001001
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop

set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept

delete interface ge-0/0/0.0
set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 mtu 9000
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 200.200.1.0/31
set interfaces ge-0/0/0 unit 101 family inet6 address 2001:dead:beef:2001::/127

## configuration for PE12

set routing-options resolution preserve-nexthop-hierarchy
set routing-options router-id 192.168.0.12
set routing-options autonomous-system 4200000001

set protocols bgp group to_int type internal
set protocols bgp group to_int local-address bad:cafe::12
set protocols bgp group to_int family inet unicast extended-nexthop
set protocols bgp group to_int family inet unicast advertise-srv6-service
set protocols bgp group to_int family inet unicast accept-srv6-service
set protocols bgp group to_int family inet6 unicast advertise-srv6-service
set protocols bgp group to_int family inet6 unicast accept-srv6-service
set protocols bgp group to_int export to_int
set protocols bgp group to_int neighbor bad:cafe::11
set protocols bgp group to_ce2 neighbor 200.200.1.3 peer-as 4200001002
set protocols bgp group to_ce2 neighbor 2001:dead:beef:2001::3 peer-as 4200001002
set protocols bgp source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set protocols bgp rfc6514-compliant-safi129
set protocols bgp multipath list-nexthop

set policy-options policy-statement to_int term 1 then next-hop self
set policy-options policy-statement to_int term 1 then accept

delete interface ge-0/0/0.0
set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 mtu 9000
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 200.200.1.2/31
set interfaces ge-0/0/0 unit 101 family inet6 address 2001:dead:beef:2001::2/127


