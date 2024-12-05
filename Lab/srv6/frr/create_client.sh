#!/bin/bash
# for i in c{1..4}evpn1
# do
#     echo "creating LXC ${i}"
#     lxc copy client ${i}
# done


sudo apt install openvswitch-common openvswitch-switch

cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  bridges:
    ovs1:
      openvswitch: {}
      interfaces:
      - eth1
    ovs2:
      openvswitch: {}
      interfaces:
      - eth2
EOF
sudo netplan apply


lxc image copy images:alpine/edge local: --alias alpine

lxc launch alpine alpine
lxc exec alpine sh

apk update
apk upgrade
apk add openssh iperf iperf3 curl python3
rc-update add sshd
service sshd start
ssh-keygen -t rsa
cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys

lxc stop alpine


export LXC_NAME=c2
export VLAN=101
export OVS=ovs2
echo "Creating container ${LXC_NAME}"
lxc copy alpine ${LXC_NAME}
lxc query --request PATCH /1.0/instances/${LXC_NAME} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${OVS}\",
       \"vlan\" : \"${VLAN}\",
       \"type\": \"nic\"
    }
  }
}"

lxc start ${LXC_NAME}


cat << EOF | sudo tee /etc/radvd.conf

interface eth3.101
{
	AdvSendAdvert on;
	MinRtrAdvInterval 30;
	MaxRtrAdvInterval 100;
	prefix fc00:dead:beef:a012::/64
	{
		AdvOnLink on;
		AdvAutonomous on;
		AdvRouterAddr on;
	};
};
EOF
sudo systemctl restart radvd

cat << EOF | sudo tee /etc/dhcp/dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
subnet 192.168.12.0 netmask 255.255.255.0 {
   range 192.168.12.11 192.168.12.200;
   option routers 192.168.12.1;
}
EOF



cat << EOF | sudo tee /etc/dhcp/dhcpd6.conf
default-lease-time 2592000;
preferred-lifetime 604800;
option dhcp-renewal-time 3600;
option dhcp-rebinding-time 7200;
allow leasequery;
option dhcp6.info-refresh-time 21600;
subnet6 fc00:dead:beef:a012::/64 {
    range6 fc00:dead:beef:a012::1000:1 fc00:dead:beef:a012::1000:ffff;
}
EOF

sudo systemctl restart isc-dhcp-server


EOF

sudo systemctl enable isc-dhcp-server frr lldpd radvd
sudo systemctl start isc-dhcp-server frr lldpd radvd



for i in ubuntu@172.16.10.{1..4}
do
  scp ./junos-routing-crpd-docker-amd64-24.2R1.14.tgz ${i}:~/
done
