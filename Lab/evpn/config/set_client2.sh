sudo ip netns add pe1
sudo ip link set dev eth1 netns pe1
sudo ip netns exec pe1 ip link set dev lo up
sudo ip netns exec pe1 ip link add link eth1 name pe1101 type vlan id 101
sudo ip netns exec pe1 ip addr add dev pe1101 10.1.111.11/24
sudo ip netns exec pe1 ip link set dev eth1 up
sudo ip netns exec pe1 ip link set dev pe1101 up
sudo ip netns exec pe1 ip route add default via 10.1.111.1

sudo ip netns add pe2
sudo ip link set dev eth2 netns pe2
sudo ip netns exec pe2 ip link set dev lo up
sudo ip netns exec pe2 ip link add link eth2 name pe2102 type vlan id 102
sudo ip netns exec pe2 ip addr add dev pe2102 10.1.112.12/24
sudo ip netns exec pe2 ip link set dev eth2 up
sudo ip netns exec pe2 ip link set dev pe2102 up
sudo ip netns exec pe2 ip route add default via 10.1.112.1

sudo ip netns add pe3
sudo ip link set dev eth3 netns pe3
sudo ip netns exec pe3 ip link set dev lo up
sudo ip netns exec pe3 ip link add link eth3 name pe3102 type vlan id 102
sudo ip netns exec pe3 ip addr add dev pe3102 10.1.112.13/24
sudo ip netns exec pe3 ip link set dev eth3 up
sudo ip netns exec pe3 ip link set dev pe3102 up
sudo ip netns exec pe3 ip route add default via 10.1.112.1

alias pe1="sudo ip netns exec pe1"
alias pe2="sudo ip netns exec pe2"
alias pe3="sudo ip netns exec pe3"



