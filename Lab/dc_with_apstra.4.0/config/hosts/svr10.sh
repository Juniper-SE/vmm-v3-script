NETNS=c1
INTF=eth1
VLANID=107
IPADDR=192.168.112.10/24
GATEWAY=192.168.112.1
VLANINTF=c1v107
sudo ip link add link ${INTF} name c1v107 type vlan id 107
sudo ip link set dev ${INTF} up
sudo ip netns add ${NETNS}
sudo ip link set dev c1v107 netns ${NETNS}
sudo ip netns exec ${NETNS} ip link set dev lo up
sudo ip netns exec ${NETNS} ip addr add dev ${VLANINTF} ${IPADDR}
sudo ip netns exec ${NETNS} ip link set dev ${VLANINTF} up
sudo ip netns exec ${NETNS} ip route add default via ${GATEWAY}
alias c1="sudo ip netns exec ${NETNS}"