yum -y install epel-release
yum -y update
yum -y install dnsmasq nginx dhcp
# systemctl start dnsmasq
systemctl enable dnsmasq
# systemctl start dhcpd
systemctl enable dhcpd
cp ./dhcpd.conf /etc/dhcp/dhcpd.conf
cp ./route-eth2 /etc/sysconfig/network-scripts/
echo "server ntp.juniper.net iburst" >> /etc/chrony.conf
echo "allow 172.16.0.0/16" >> /etc/chrony.conf
systemctl enable chronyd
systemctl enable nginx
mkdir /usr/share/nginx/html/file/
cp nginx.conf /etc/nginx/nginx.conf
echo "addn-hosts=/etc/dns_data" >> /etc/dnsmasq.conf
echo "172.16.20.11 netround" >> /etc/dns_data
echo "172.16.20.12 hb" >> /etc/dns_data
echo "172.16.20.13 ns" >> /etc/dns_data
echo "Reboot server"
reboot
