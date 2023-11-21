sudo apt -y update 
sudo apt -y upgrade
sudo apt -y install isc-dhcp-server

cat << EOF | sudo tee /etc/dhcp/dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
subnet 172.17.1.0 netmask 255.255.255.0 {
   range 172.17.1.11 172.17.1.100;
   option routers 172.17.1.1;
   option domain-name-servers 66.129.233.81;
}
subnet 172.17.2.0 netmask 255.255.255.0 {
   range 172.17.2.11 172.17.2.100;
   option routers 172.17.2.1;
   option domain-name-servers 66.129.233.81;
}
subnet 172.17.3.0 netmask 255.255.255.0 {
   range 172.17.3.11 172.17.3.100;
   option routers 172.17.3.1;
   option domain-name-servers 66.129.233.81;
}
subnet 172.17.100.0 netmask 255.255.255.0 {
   range 172.17.100.11 172.17.100.100;
   option routers 172.17.100.1;
   option domain-name-servers 66.129.233.81;
}
EOF

sudo systemctl restart isc-dhcp-server
sudo sed -i -e '/forward/ d' /etc/sysctl.conf
cat << EOF | sudo tee -a /etc/sysctl.conf
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
EOF

sudo sysctl -f /etc/sysctl.conf

