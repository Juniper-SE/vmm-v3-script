yum -y install epel-release
yum -y update
yum -y install dnsmasq nginx
systemctl start dnsmasq
systemctl enable dnsmasq
echo "server ntp.juniper.net iburst" >> /etc/chrony.conf
echo "allow 172.16.0.0/16" >> /etc/chrony.conf
systemctl enable chronyd
systemctl enable nginx
mkdir /usr/share/nginx/html/file/
cp nginx.conf /etc/nginx/nginx.conf
echo "dhcp-range=172.16.10.60,172.16.10.80,255.255.255.0,2h" >> /etc/dnsmasq.conf
echo "addn-hosts=/etc/dns_data" >> /etc/dnsmasq.conf
echo "172.16.10.200 vcsa" >> /etc/dns_data
echo "172.16.10.201 esxi1" >> /etc/dns_data
echo "172.16.10.202 esxi2" >> /etc/dns_data
echo "172.16.10.203 esxi3" >> /etc/dns_data
echo "Reboot server"
reboot
