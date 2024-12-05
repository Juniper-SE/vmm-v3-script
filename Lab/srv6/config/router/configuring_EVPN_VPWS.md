# Configuring EVPN-VPWS using SRv6

## configuration for PE11

set interfaces ge-0/0/0 unit 102 vlan-id 102
set interfaces ge-0/0/0 unit 102 encapsulation vlan-ccc
set interfaces ge-0/0/0 unit 102 vlan-id 102
set routing-instances evpn_vpws1 instance-type evpn-vpws
set routing-instances evpn_vpws1 protocols evpn interface ge-0/0/0.102 vpws-service-id local 102
set routing-instances evpn_vpws1 protocols evpn interface ge-0/0/0.102 vpws-service-id remote 102
set routing-instances evpn_vpws1 protocols evpn interface ge-0/0/0.102 vpws-service-id source-packet-routing srv6 locator SRV6-LOC-1
set routing-instances evpn_vpws1 protocols evpn encapsulation srv6
set routing-instances evpn_vpws1 interface ge-0/0/0.102
set routing-instances evpn_vpws1 vrf-target target:65412:1102
set protocols bgp group to_int family evpn signaling advertise-srv6-service
set protocols bgp group to_int family evpn signaling accept-srv6-service


## configuration for PE12

set interfaces ge-0/0/0 unit 102 vlan-id 102
set interfaces ge-0/0/0 unit 102 encapsulation vlan-ccc
set interfaces ge-0/0/0 unit 102 vlan-id 102
set routing-instances evpn_vpws1 instance-type evpn-vpws
set routing-instances evpn_vpws1 protocols evpn interface ge-0/0/0.102 vpws-service-id local 102
set routing-instances evpn_vpws1 protocols evpn interface ge-0/0/0.102 vpws-service-id remote 102
set routing-instances evpn_vpws1 protocols evpn interface ge-0/0/0.102 vpws-service-id source-packet-routing srv6 locator SRV6-LOC-1
set routing-instances evpn_vpws1 protocols evpn encapsulation srv6
set routing-instances evpn_vpws1 interface ge-0/0/0.102
set routing-instances evpn_vpws1 vrf-target target:65412:1102
set protocols bgp group to_int family evpn signaling advertise-srv6-service
set protocols bgp group to_int family evpn signaling accept-srv6-service

