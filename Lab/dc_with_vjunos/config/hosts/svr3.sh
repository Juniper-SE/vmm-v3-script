NETNS=VRF2
INTF=eth3
VLANID=101
IPADDR=192.168.112.13/24
GATEWAY=192.168.112.1
sudo ip netns add ${NETNS}
sudo ip link set dev ${INTF} netns ${NETNS}
sudo ip netns exec ${NETNS} ip link set dev lo up
sudo ip netns exec ${NETNS} ip addr add dev ${INTF} ${IPADDR}
sudo ip netns exec ${NETNS} ip link set dev ${INTF} up
sudo ip netns exec ${NETNS} ip route add default via ${GATEWAY}
alias VRF2="sudo ip netns exec ${NETNS}"