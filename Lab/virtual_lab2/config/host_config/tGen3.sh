#!/bin/bash
## configuration on tGEN



sudo ip link add link eth1 name eth1.1 type vlan id 1
sudo ip netns exec vrf1_eth1 ip link set dev lo up
sudo ip link set dev eth1.1 netns vrf1_eth1
sudo ip netns exec vrf1_eth1 ip link set dev eth1.1 up
sudo ip netns exec vrf1_eth1 ip addr add dev eth1.1 200.1.0.2/24
sudo ip netns exec vrf1_eth1 ip route add default via 200.1.0.1
sudo ip netns exec vrf1_eth1 ip -6 addr add dev eth1.1 2001:dead:beef:1000::2/64
sudo ip netns exec vrf1_eth1 ip -6 route add ::/0 via 2001:dead:beef:1000::1

sudo ip link add link eth2 name eth2.1 type vlan id 1
sudo ip netns exec vrf2_eth2 ip link set dev lo up
sudo ip link set dev eth2.1 netns vrf2_eth2
sudo ip netns exec vrf2_eth2 ip link set dev eth2.1 up
sudo ip netns exec vrf2_eth2 ip addr add dev eth2.1 200.2.0.2/24
sudo ip netns exec vrf2_eth2 ip route add default via 200.2.0.1
sudo ip netns exec vrf2_eth2 ip -6 addr add dev eth2.1 2001:dead:beef:2000::2/64
sudo ip netns exec vrf2_eth2 ip -6 route add ::/0 via 2001:dead:beef:2000::1

sudo ip link add link eth3 name eth3.1 type vlan id 1
sudo ip netns exec vrf3_eth3 ip link set dev lo up
sudo ip link set dev eth3.1 netns vrf3_eth3
sudo ip netns exec vrf3_eth3 ip link set dev eth3.1 up
sudo ip netns exec vrf3_eth3 ip addr add dev eth3.1 200.3.0.2/24
sudo ip netns exec vrf3_eth3 ip route add default via 200.3.0.1
sudo ip netns exec vrf3_eth3 ip -6 addr add dev eth3.1 2001:dead:beef:3000::2/64
sudo ip netns exec vrf3_eth3 ip -6 route add ::/0 via 2001:dead:beef:3000::1

sudo ip link add link eth4 name eth4.1 type vlan id 1
sudo ip netns exec vrf4_eth4 ip link set dev lo up
sudo ip link set dev eth4.1 netns vrf4_eth4
sudo ip netns exec vrf4_eth4 ip link set dev eth4.1 up
sudo ip netns exec vrf4_eth4 ip addr add dev eth4.1 200.4.0.2/24
sudo ip netns exec vrf4_eth4 ip route add default via 200.4.0.1
sudo ip netns exec vrf4_eth4 ip -6 addr add dev eth4.1 2001:dead:beef:4000::2/64
sudo ip netns exec vrf4_eth4 ip -6 route add ::/0 via 2001:dead:beef:4000::1



sudo ip link add link eth1 name eth1.10 type vlan id 10
sudo ip netns exec cust1_eth1 ip link set dev lo up
sudo ip link set dev eth1.10 netns cust1_eth1
sudo ip netns exec cust1_eth1 ip link set dev eth1.10 up
sudo ip netns exec cust1_eth1 ip addr add dev eth1.10 192.168.11.10/24
sudo ip netns exec cust1_eth1 ip route add default via 192.168.11.1
sudo ip netns exec cust1_eth1 ip -6 addr add dev eth1.10 2001:dead:beef:1011::10/64
sudo ip netns exec cust1_eth1 ip -6 route add default via 2001:dead:beef:1011::1

sudo ip link add link eth2 name eth2.10 type vlan id 10
sudo ip netns exec cust1_eth2 ip link set dev lo up
sudo ip link set dev eth2.10 netns cust1_eth2
sudo ip netns exec cust1_eth2 ip link set dev eth2.10 up
sudo ip netns exec cust1_eth2 ip addr add dev eth2.10 192.168.12.10/24
sudo ip netns exec cust1_eth2 ip route add default via 192.168.12.1
sudo ip netns exec cust1_eth2 ip -6 addr add dev eth2.10 2001:dead:beef:1012::10/64
sudo ip netns exec cust1_eth2 ip -6 route add default via 2001:dead:beef:1012::1


sudo ip link add link eth3 name eth3.10 type vlan id 10
sudo ip netns exec cust1_eth3 ip link set dev lo up
sudo ip link set dev eth3.10 netns cust1_eth3
sudo ip netns exec cust1_eth3 ip link set dev eth3.10 up
sudo ip netns exec cust1_eth3 ip addr add dev eth3.10 192.168.13.10/24
sudo ip netns exec cust1_eth3 ip route add default via 192.168.13.1
sudo ip netns exec cust1_eth3 ip -6 addr add dev eth3.10 2001:dead:beef:1013::10/64
sudo ip netns exec cust1_eth3 ip -6 route add default via 2001:dead:beef:1013::1

sudo ip link add link eth4 name eth4.10 type vlan id 10
sudo ip netns exec cust1_eth4 ip link set dev lo up
sudo ip link set dev eth4.10 netns cust1_eth4
sudo ip netns exec cust1_eth4 ip link set dev eth4.10 up
sudo ip netns exec cust1_eth4 ip addr add dev eth4.10 192.168.14.10/24
sudo ip netns exec cust1_eth4 ip route add default via 192.168.14.1
sudo ip netns exec cust1_eth4 ip -6 addr add dev eth4.10 2001:dead:beef:1014::10/64
sudo ip netns exec cust1_eth4 ip -6 route add default via 2001:dead:beef:1014::1

