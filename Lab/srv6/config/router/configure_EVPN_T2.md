# Configuring EVPN T2 using SRv6

## configuration for PE11

set routing-instances EVPN1 instance-type mac-vrf
set routing-instances EVPN1 protocols evpn encapsulation srv6
set routing-instances EVPN1 protocols evpn source-packet-routing srv6 locator SRV6-LOC-1
set routing-instances EVPN1 protocols evpn source-packet-routing srv6 locator end-dt2-sid
set routing-instances EVPN1 bridge-domains bd10 domain-type bridge
set routing-instances EVPN1 bridge-domains bd10 vlan-id 103
set routing-instances EVPN1 bridge-domains bd10 interface ge-0/0/0.103
set routing-instances EVPN1 service-type vlan-based
set routing-instances EVPN1 interface ge-0/0/0.103
set routing-instances EVPN1 vrf-target target:65412:1103
set interfaces ge-0/0/0 unit 103 encapsulation vlan-bridge
set interfaces ge-0/0/0 unit 103 vlan-id 103

## configuration for PE12


set routing-instances EVPN1 instance-type mac-vrf
set routing-instances EVPN1 protocols evpn encapsulation srv6
set routing-instances EVPN1 protocols evpn source-packet-routing srv6 locator SRV6-LOC-1
set routing-instances EVPN1 protocols evpn source-packet-routing srv6 locator end-dt2-sid
set routing-instances EVPN1 bridge-domains bd10 domain-type bridge
set routing-instances EVPN1 bridge-domains bd10 vlan-id 103
set routing-instances EVPN1 bridge-domains bd10 interface ge-0/0/0.103
set routing-instances EVPN1 service-type vlan-based
set routing-instances EVPN1 interface ge-0/0/0.103
set routing-instances EVPN1 vrf-target target:65412:1103
set interfaces ge-0/0/0 unit 103 encapsulation vlan-bridge
set interfaces ge-0/0/0 unit 103 vlan-id 103

