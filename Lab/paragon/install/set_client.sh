
NETNS="r1vlan1"
IPADDR="192.168.1.10/24"
GATEWAY4="192.168.1.1"
VLAN="1"
INTF="eth1"
ip netns add ${NETNS}
ip link add link ${INTF} name ${NETNS} type vlan id ${VLAN}
ip link set dev ${NETNS} netns ${NETNS}
ip netns exec ${NETNS} ip addr add  dev ${NETNS} ${IPADDR}
ip netns exec ${NETNS} ip link set dev lo up
ip netns exec ${NETNS} ip link set dev ${NETNS} up
ip netns exec ${NETNS} ip route add 0/0 via ${GATEWAY4}
NETNS="r1vlan2"
IPADDR="192.168.3.10/24"
GATEWAY4="192.168.3.1"
VLAN="2"
INTF="eth1"
ip netns add ${NETNS}
ip link add link ${INTF} name ${NETNS} type vlan id ${VLAN}
ip link set dev ${NETNS} netns ${NETNS}
ip netns exec ${NETNS} ip addr add  dev ${NETNS} ${IPADDR}
ip netns exec ${NETNS} ip link set dev lo up
ip netns exec ${NETNS} ip link set dev ${NETNS} up
ip netns exec ${NETNS} ip route add 0/0 via ${GATEWAY4}
NETNS="r7vlan1"
IPADDR="192.168.2.10/24"
GATEWAY4="192.168.2.1"
VLAN="1"
INTF="eth7"
ip netns add ${NETNS}
ip link add link ${INTF} name ${NETNS} type vlan id ${VLAN}
ip link set dev ${NETNS} netns ${NETNS}
ip netns exec ${NETNS} ip addr add  dev ${NETNS} ${IPADDR}
ip netns exec ${NETNS} ip link set dev lo up
ip netns exec ${NETNS} ip link set dev ${NETNS} up
ip netns exec ${NETNS} ip route add 0/0 via ${GATEWAY4}
NETNS="r7vlan2"
IPADDR="192.168.4.10/24"
GATEWAY4="192.168.4.1"
VLAN="2"
INTF="eth7"
ip netns add ${NETNS}
ip link add link ${INTF} name ${NETNS} type vlan id ${VLAN}
ip link set dev ${NETNS} netns ${NETNS}
ip netns exec ${NETNS} ip addr add  dev ${NETNS} ${IPADDR}
ip netns exec ${NETNS} ip link set dev lo up
ip netns exec ${NETNS} ip link set dev ${NETNS} up
ip netns exec ${NETNS} ip route add 0/0 via ${GATEWAY4}





alias r1v1='sudo ip netns exec r1vlan1'
alias r1v2='sudo ip netns exec r1vlan2'
alias r7v1='sudo ip netns exec r7vlan1'
alias r7v2='sudo ip netns exec r7vlan2'





set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 1 vlan-id 1
set interfaces ge-0/0/0 unit 1 family inet address 192.168.1.1/24
set routing-options static route 192.168.2.0/24 lsp-next-hop LSP1

set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 2 vlan-id 2
set interfaces ge-0/0/0 unit 2 family inet address 192.168.3.1/24
set routing-options static route 192.168.4.0/24 lsp-next-hop LSP2


set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 1 vlan-id 1
set interfaces ge-0/0/0 unit 1 family inet address 192.168.2.1/24
set routing-options static route 192.168.1.0/24 lsp-next-hop LSP1

set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 unit 2 vlan-id 2
set interfaces ge-0/0/0 unit 2 family inet address 192.168.4.1/24
set routing-options static route 192.168.3.0/24 lsp-next-hop LSP2