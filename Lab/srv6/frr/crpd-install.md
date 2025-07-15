## Installing CRI-O and podman

export CRIO_VERSION=v1.30
curl -fsSL https://pkgs.k8s.io/addons:/cri-o:/stable:/$CRIO_VERSION/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/cri-o-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/cri-o-apt-keyring.gpg] https://pkgs.k8s.io/addons:/cri-o:/stable:/$CRIO_VERSION/deb/ /" | sudo tee /etc/apt/sources.list.d/cri-o.list

sudo apt -y update
sudo apt -y upgrade
sudo apt install -y cri-o podman lldpd
sudo systemctl start crio.service

## installing cRPD
podman load -i junos-routing-crpd-docker-amd64-24.2R1.14.tgz
export CRPD_NAME=crpd1
sudo podman volume create ${CRPD_NAME}-config
sudo podman volume create ${CRPD_NAME}-varlog

export CRPD_NAME=crpd1
sudo podman run --rm --detach --name ${CRPD_NAME} -h ${CRPD_NAME} \
       --net=host --privileged \
       -v ${CRPD_NAME}-config:/config \
       -v ${CRPD_NAME}-varlog:/var/log \
       -it localhost/crpd:24.2R1.14

sudo podman ps -a


## installing on PE11

cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  vlans:
    eth3.101:
      dhcp4: false
      id: 101
      link: eth3
      addresses:
        - 192.168.11.1/24
        - fc00:dead:beef:a011::1/64 
EOF

sudo netplan apply

cat << EOF | sudo tee /etc/dhcp/dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
subnet 192.168.11.0 netmask 255.255.255.0 {
 range 192.168.11.11 192.168.11.100;
 option routers 192.168.11.1;
}
EOF
sudo systemctl restart isc-dhcp-server 

cat << EOF | sudo tee /etc/radvd.conf
interface eth3.101
{
	AdvSendAdvert on;
	MinRtrAdvInterval 30;
	MaxRtrAdvInterval 100;
	prefix fc00:dead:beef:a011::/64
	{
		AdvOnLink on;
		AdvAutonomous on;
		AdvRouterAddr on;
	};
};
EOF
sudo systemctl restart radvd


## installing on PE12

cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  vlans:
    eth3.101:
      dhcp4: false
      id: 101
      link: eth3
      addresses:
        - 192.168.12.1/24
        - fc00:dead:beef:a012::1/64 
EOF

sudo netplan apply

cat << EOF | sudo tee /etc/dhcp/dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
subnet 192.168.12.0 netmask 255.255.255.0 {
 range 192.168.12.11 192.168.12.100;
 option routers 192.168.12.1;
}
EOF
sudo systemctl restart isc-dhcp-server 

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



# cRPD configuration ipv4/ipv6 routing with ISIS

## PE11
set interfaces lo0 unit 0 family iso address 49.0001.0001.0011.00
set policy-options policy-statement lb then load-balance per-flow
set routing-options forwarding-table export lb
set protocols isis interface eth1 point-to-point
set protocols isis interface eth2 point-to-point
set protocols isis interface eth3.101 passive

## PE12
set interfaces lo0 unit 0 family iso address 49.0001.0001.0012.00
set policy-options policy-statement lb then load-balance per-flow
set routing-options forwarding-table export lb
set protocols isis interface eth1 point-to-point
set protocols isis interface eth2 point-to-point
set protocols isis interface eth3.101 passive

## P1
set interfaces lo0 unit 0 family iso address 49.0001.0001.0001.00
set policy-options policy-statement lb then load-balance per-flow
set routing-options forwarding-table export lb
set protocols isis interface eth1 point-to-point
set protocols isis interface eth2 point-to-point

## P2
set interfaces lo0 unit 0 family iso address 49.0001.0001.0001.00
set policy-options policy-statement lb then load-balance per-flow
set routing-options forwarding-table export lb
set protocols isis interface eth1 point-to-point
set protocols isis interface eth2 point-to-point


# Enabling MPLS on linux

sudo modprobe mpls_router
sudo modprobe mpls_iptunnel
sudo modprobe mpls_gso
sudo modprobe dummy

cat << EOF | sudo tee /etc/modules-load.d/10_mpls.conf
mpls_router
mpls_iptunnel
mpls_gso
dummy
EOF

cat << EOF | sudo tee /etc/sysctl.d/90-mpls-router.conf
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
net.ipv4.conf.all.rp_filter=0
net.mpls.platform_labels=1048575
net.ipv4.tcp_l3mdev_accept=1
net.ipv4.udp_l3mdev_accept=1
net.mpls.conf.lo.input=1
EOF
sudo sysctl -p /etc/sysctl.d/90-mpls-router.conf


## configure startup for PE11

cat << EOF | sudo tee /etc/systemd/system/rc.local.service

[Unit]
Description=RC local service
After=network.target auditd.service

[Service]
ExecStart=/usr/local/bin/startup.sh

[Install]
WantedBy=multi-user.target
EOF

cat << EOF | sudo tee /usr/local/bin/startup.sh
#!/bin/bash
ip link add dev dummy0 type dummy
ip link set dev dummy0 up
ip addr add dev dummy0 192.168.255.11/32
ip link add customer1 type vrf table 100
ip link set customer1 up
ip route add vrf customer1 unreachable default metric 4278198272
ip link set eth3.101 vrf customer1
sysctl net.mpls.conf.eth1.input=1
sysctl net.mpls.conf.eth2.input=1
exit 0
EOF
sudo chmod +x /usr/local/bin/startup.sh

sudo systemctl enable rc.local.service
sudo systemctl start rc.local.service


## configure startup for PE12

cat << EOF | sudo tee /etc/systemd/system/rc.local.service

[Unit]
Description=RC local service
After=network.target auditd.service

[Service]
ExecStart=/usr/local/bin/startup.sh

[Install]
WantedBy=multi-user.target
EOF

cat << EOF | sudo tee /usr/local/bin/startup.sh
#!/bin/bash
ip link add dev dummy0 type dummy
ip link set dev dummy0 up
ip addr add dev dummy0 192.168.255.12/32
ip link add customer1 type vrf table 100
ip link set customer1 up
ip route add vrf customer1 unreachable default metric 4278198272
ip link set eth3.101 vrf customer1
sysctl net.mpls.conf.eth1.input=1
sysctl net.mpls.conf.eth2.input=1
exit 0
EOF
sudo chmod +x /usr/local/bin/startup.sh

sudo systemctl enable rc.local.service
sudo systemctl start rc.local.service


## configure startup for P1

cat << EOF | sudo tee /etc/systemd/system/rc.local.service

[Unit]
Description=RC local service
After=network.target auditd.service

[Service]
ExecStart=/usr/local/bin/startup.sh

[Install]
WantedBy=multi-user.target
EOF

cat << EOF | sudo tee /usr/local/bin/startup.sh
#!/bin/bash
ip link add dev dummy0 type dummy
ip link set dev dummy0 up
ip addr add dev dummy0 192.168.255.1/32
sysctl net.mpls.conf.eth1.input=1
sysctl net.mpls.conf.eth2.input=1
exit 0
EOF
sudo chmod +x /usr/local/bin/startup.sh

sudo systemctl enable rc.local.service
sudo systemctl start rc.local.service



## configure startup for P2

cat << EOF | sudo tee /etc/systemd/system/rc.local.service

[Unit]
Description=RC local service
After=network.target auditd.service

[Service]
ExecStart=/usr/local/bin/startup.sh

[Install]
WantedBy=multi-user.target
EOF

cat << EOF | sudo tee /usr/local/bin/startup.sh
#!/bin/bash
ip link add dev dummy0 type dummy
ip link set dev dummy0 up
ip addr add dev dummy0 192.168.255.2/32
sysctl net.mpls.conf.eth1.input=1
sysctl net.mpls.conf.eth2.input=1
exit 0
EOF
sudo chmod +x /usr/local/bin/startup.sh

sudo systemctl enable rc.local.service
sudo systemctl start rc.local.service



set routing-instances customer1 instance-type vrf
set routing-instances customer1 interface eth3.101
set routing-instances customer1 vrf-target target:65001:1001
set routing-instances customer1 vrf-table-label
set routing-options route-distinguisher-id 192.168.255.12
delete protocols isis interface eth3.101




set system ntp server 66.129.233.81
set system name-server 10.49.32.95
set system name-server 10.49.32.97