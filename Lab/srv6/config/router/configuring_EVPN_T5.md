# Configuring EVPN T5 using SRv6

## configuration for PE11

set routing-instances evpn_vrf1 instance-type vrf
set routing-instances evpn_vrf1 protocols bgp group to_ce5 export from_evpn
set routing-instances evpn_vrf1 protocols bgp group to_ce5 neighbor 192.168.255.1 peer-as 4200002001
set routing-instances evpn_vrf1 protocols bgp group to_ce5 neighbor fc00:dead:beef:ffff::1 peer-as 4200002001
set routing-instances evpn_vrf1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances evpn_vrf1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances evpn_vrf1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances evpn_vrf1 interface ge-0/0/0.104
set routing-instances evpn_vrf1 vrf-target target:65412:1104
set routing-instances evpn_vrf1 vrf-table-label

set interfaces ge-0/0/0 unit 104 vlan-id 104
set interfaces ge-0/0/0 unit 104 family inet address 192.168.255.0/31
set interfaces ge-0/0/0 unit 104 family inet6 address fc00:dead:beef:ffff::0/127

set policy-options policy-statement from_evpn term 1 from protocol evpn
set policy-options policy-statement from_evpn term 1 then accept



## configuration for PE12


set routing-instances evpn_vrf1 instance-type vrf
set routing-instances evpn_vrf1 protocols bgp group to_ce6 export from_evpn
set routing-instances evpn_vrf1 protocols bgp group to_ce6 neighbor 192.168.255.3 peer-as 4200002002
set routing-instances evpn_vrf1 protocols bgp group to_ce6 neighbor fc00:dead:beef:ffff::3 peer-as 4200002002
set routing-instances evpn_vrf1 protocols evpn ip-prefix-routes advertise direct-nexthop
set routing-instances evpn_vrf1 protocols evpn ip-prefix-routes encapsulation srv6
set routing-instances evpn_vrf1 protocols evpn ip-prefix-routes source-packet-routing srv6 locator SRV6-LOC-1 end-dt46-sid
set routing-instances evpn_vrf1 interface ge-0/0/0.104
set routing-instances evpn_vrf1 vrf-target target:65412:1104
set routing-instances evpn_vrf1 vrf-table-label

set interfaces ge-0/0/0 unit 104 vlan-id 104
set interfaces ge-0/0/0 unit 104 family inet address 192.168.255.2/31
set interfaces ge-0/0/0 unit 104 family inet6 address fc00:dead:beef:ffff::2/127

set policy-options policy-statement from_evpn term 1 from protocol evpn
set policy-options policy-statement from_evpn term 1 then accept



