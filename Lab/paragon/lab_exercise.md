# this is the lab exercise
R1 configuration

set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 1 vlan-id 1
set interfaces ge-0/0/0 unit 1 family inet address 10.1.71.1/24
set routing-options static route 10.1.76.0/24 lsp-next-hop LSP1


alias r1v1="sudo ip netns exec r1v1"
sudo ip netns add r1v1
sudo ip link set dev r1v1 netns r1v1
r1v1 ip link set dev lo up
r1v1 ip link set dev r1v1 up
r1v1 ip addr add dev r1v1 10.1.71.2/24
r1v1 ip route add default via 10.1.71.1


R6 configuration
set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 1 vlan-id 1
set interfaces ge-0/0/0 unit 1 family inet address 10.1.76.1/24
set routing-options static route 10.1.71.0/24 lsp-next-hop LSP1


alias r6v1="sudo ip netns exec r6v1"
sudo ip netns add r6v1
sudo ip link set dev r6v1 netns r6v1
r6v1 ip link set dev lo up
r6v1 ip link set dev r6v1 up
r6v1 ip addr add dev r6v1 10.1.76.2/24
r6v1 ip route add default via 10.1.76.1





## ssh configuration
ssh -i pchome.pem -p 65133 -f -N -R 65022:localhost:65022 irzan@debian1.irzan.com


## alias command
alias cust1a="sudo ip netns exec cust1a"
alias cust1b="sudo ip netns exec cust1b"

## host ci
VLAN=101
INTF=eth1
VINTF=cust1a
NS=${VINTF}
alias cust1a="sudo ip netns exec ${NS}"
sudo ip link add link ${INTF} name ${VINTF} type vlan id ${VLAN}
sudo ip netns add ${NS}
sudo ip link set dev ${NS} netns ${NS}
cust1a ip link set dev lo up
cust1a ip link set dev ${NS} up
cust1a ip addr add dev ${NS} 10.1.201.2/24
cust1a ip route add default via 10.1.201.1

VLAN=101
INTF=eth2
VINTF=cust1b
NS=${VINTF}
alias cust1b="sudo ip netns exec ${NS}"
sudo ip link add link ${INTF} name ${VINTF} type vlan id ${VLAN}
sudo ip netns add ${NS}
sudo ip link set dev ${NS} netns ${NS}
cust1b ip link set dev lo up
cust1b ip link set dev ${NS} up
cust1b ip addr add dev ${NS} 10.1.202.2/24
cust1b ip route add default via 10.1.202.1

## node pei1

set routing-options route-distinguisher-id 10.100.1.133
set routing-options autonomous-system 65001

set protocols bgp group to_rr type internal
set protocols bgp group to_rr local-address 10.100.1.133
set protocols bgp group to_rr family inet-vpn any
set protocols bgp group to_rr neighbor 10.100.1.102

set routing-instances cust1 instance-type vrf
set routing-instances cust1 interface ge-0/0/0.101
set routing-instances cust1 vrf-target target:65001:10001
set routing-instances cust1 vrf-table-label


set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 1 vlan-id 101
set interfaces ge-0/0/0 unit 1 family inet address 10.1.201.1/24


## node pei2

set routing-options route-distinguisher-id 10.100.1.134
set routing-options autonomous-system 65001

set protocols bgp group to_rr type internal
set protocols bgp group to_rr local-address 10.100.1.134
set protocols bgp group to_rr family inet-vpn any
set protocols bgp group to_rr neighbor 10.100.1.102

set routing-instances cust1 instance-type vrf
set routing-instances cust1 interface ge-0/0/0.101
set routing-instances cust1 vrf-target target:65001:10001
set routing-instances cust1 vrf-table-label

set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 10.1.202.1/24


## node cx2

set routing-options autonomous-system 65001

set protocols bgp group to_client type internal
set protocols bgp group to_client local-address 10.100.1.102
set protocols bgp group to_client family inet-vpn any
set protocols bgp group to_client cluster 10.100.1.102



## host cz
VLAN=101
INTF=eth1
VINTF=cust1a
NS=${VINTF}
alias cust1a="sudo ip netns exec ${NS}"
sudo ip link add link ${INTF} name ${VINTF} type vlan id ${VLAN}
sudo ip netns add ${NS}
sudo ip link set dev ${NS} netns ${NS}
cust1a ip link set dev lo up
cust1a ip link set dev ${NS} up
cust1a ip addr add dev ${NS} 10.1.203.2/24
cust1a ip route add default via 10.1.203.1

VLAN=101
INTF=eth2
VINTF=cust1b
NS=${VINTF}
alias cust1b="sudo ip netns exec ${NS}"
sudo ip link add link ${INTF} name ${VINTF} type vlan id ${VLAN}
sudo ip netns add ${NS}
sudo ip link set dev ${NS} netns ${NS}
cust1b ip link set dev lo up
cust1b ip link set dev ${NS} up
cust1b ip addr add dev ${NS} 10.1.204.2/24
cust1b ip route add default via 10.1.204.1

## node pez1

set routing-options route-distinguisher-id 10.100.1.123
set routing-options autonomous-system 65001

set protocols bgp group to_rr type internal
set protocols bgp group to_rr local-address 10.100.1.123
set protocols bgp group to_rr family inet-vpn any
set protocols bgp group to_rr neighbor 10.100.1.102

set routing-instances cust1 instance-type vrf
set routing-instances cust1 interface ge-0/0/0.101
set routing-instances cust1 vrf-target target:65001:10001
set routing-instances cust1 vrf-table-label


set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 10.1.203.1/24


## node pez2

set routing-options route-distinguisher-id 10.100.1.124
set routing-options autonomous-system 65001

set protocols bgp group to_rr type internal
set protocols bgp group to_rr local-address 10.100.1.124
set protocols bgp group to_rr family inet-vpn any
set protocols bgp group to_rr neighbor 10.100.1.102

set routing-instances cust1 instance-type vrf
set routing-instances cust1 interface ge-0/0/0.101
set routing-instances cust1 vrf-target target:65001:10001
set routing-instances cust1 vrf-table-label

set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 10.1.204.1/24



## host cy
VLAN=101
INTF=eth1
VINTF=cust1a
NS=${VINTF}
alias cust1a="sudo ip netns exec ${NS}"
sudo ip link add link ${INTF} name ${VINTF} type vlan id ${VLAN}
sudo ip netns add ${NS}
sudo ip link set dev ${NS} netns ${NS}
cust1a ip link set dev lo up
cust1a ip link set dev ${NS} up
cust1a ip addr add dev ${NS} 10.1.205.2/24
cust1a ip route add default via 10.1.205.1

VLAN=101
INTF=eth2
VINTF=cust1b
NS=${VINTF}
alias cust1b="sudo ip netns exec ${NS}"
sudo ip link add link ${INTF} name ${VINTF} type vlan id ${VLAN}
sudo ip netns add ${NS}
sudo ip link set dev ${NS} netns ${NS}
cust1b ip link set dev lo up
cust1b ip link set dev ${NS} up
cust1b ip addr add dev ${NS} 10.1.206.2/24
cust1b ip route add default via 10.1.206.1


## node pey1

set routing-options route-distinguisher-id 10.100.1.113
set routing-options autonomous-system 65001

set protocols bgp group to_rr type internal
set protocols bgp group to_rr local-address 10.100.1.113
set protocols bgp group to_rr family inet-vpn any
set protocols bgp group to_rr neighbor 10.100.1.102

set protocols ldp interface ge-0/0/1
set protocols ldp interface ge-0/0/2

set routing-instances cust1 instance-type vrf
set routing-instances cust1 interface ge-0/0/0.101
set routing-instances cust1 vrf-target target:65001:10001
set routing-instances cust1 vrf-table-label


set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 10.1.205.1/24


## node pey2

set routing-options route-distinguisher-id 10.100.1.114
set routing-options autonomous-system 65001

set protocols bgp group to_rr type internal
set protocols bgp group to_rr local-address 10.100.1.114
set protocols bgp group to_rr family inet-vpn any
set protocols bgp group to_rr neighbor 10.100.1.102

set protocols ldp interface ge-0/0/1
set protocols ldp interface ge-0/0/2

set routing-instances cust1 instance-type vrf
set routing-instances cust1 interface ge-0/0/0.101
set routing-instances cust1 vrf-target target:65001:10001
set routing-instances cust1 vrf-table-label

set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 10.1.206.1/24



## host cx
VLAN=101
INTF=eth1
VINTF=cust1a
NS=${VINTF}
alias cust1a="sudo ip netns exec ${NS}"
sudo ip link add link ${INTF} name ${VINTF} type vlan id ${VLAN}
sudo ip netns add ${NS}
sudo ip link set dev ${NS} netns ${NS}
cust1a ip link set dev lo up
cust1a ip link set dev ${NS} up
cust1a ip addr add dev ${NS} 10.1.207.2/24
cust1a ip route add default via 10.1.207.1

VLAN=101
INTF=eth2
VINTF=cust1b
NS=${VINTF}
alias cust1b="sudo ip netns exec ${NS}"
sudo ip link add link ${INTF} name ${VINTF} type vlan id ${VLAN}
sudo ip netns add ${NS}
sudo ip link set dev ${NS} netns ${NS}
cust1b ip link set dev lo up
cust1b ip link set dev ${NS} up
cust1b ip addr add dev ${NS} 10.1.208.2/24
cust1b ip route add default via 10.1.208.1


## node pex1

set routing-options route-distinguisher-id 10.100.1.103
set routing-options autonomous-system 65001

set protocols bgp group to_rr type internal
set protocols bgp group to_rr local-address 10.100.1.103
set protocols bgp group to_rr family inet-vpn any
set protocols bgp group to_rr neighbor 10.100.1.102

set protocols ldp interface ge-0/0/1
set protocols ldp interface ge-0/0/2

set routing-instances cust1 instance-type vrf
set routing-instances cust1 interface ge-0/0/0.101
set routing-instances cust1 vrf-target target:65001:10001
set routing-instances cust1 vrf-table-label


set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 10.1.207.1/24


## node pex2

set routing-options route-distinguisher-id 10.100.1.104
set routing-options autonomous-system 65001

set protocols bgp group to_rr type internal
set protocols bgp group to_rr local-address 10.100.1.104
set protocols bgp group to_rr family inet-vpn any
set protocols bgp group to_rr neighbor 10.100.1.102

set protocols ldp interface ge-0/0/1
set protocols ldp interface ge-0/0/2

set routing-instances cust1 instance-type vrf
set routing-instances cust1 interface ge-0/0/0.101
set routing-instances cust1 vrf-target target:65001:10001
set routing-instances cust1 vrf-table-label

set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 101 vlan-id 101
set interfaces ge-0/0/0 unit 101 family inet address 10.1.208.1/24







