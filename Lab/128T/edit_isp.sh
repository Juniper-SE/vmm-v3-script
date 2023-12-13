sudo sed -i -e "s/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/" /etc/sysctl.conf
sudo sed -i -e "s/#net.ipv6.conf.all.forwarding=1/net.ipv6.conf.all.forwarding=1/" /etc/sysctl.conf
sudo sysctl  -f /etc/sysctl.conf