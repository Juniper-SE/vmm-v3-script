cat << EOF | sudo tee /etc/wireguard/wg1.conf
[Interface]
PrivateKey=KHzd0OF4CfTl0gyK1Pz7j/nDrQbyxrLqK/8KWgdAfX0=
Address=192.168.198.0/31
ListenPort=17845
[Peer]
# gwnet
PublicKey=cdOoPi0T/PyjCkgSynB4K/3+ta5Ryox0DkmK9UQLrVI=
AllowedIPs=192.168.198.1/32,10.100.255.0/24,10.100.0.0/24,172.16.13.0/24,172.16.10.0/24

EOF
sudo systemctl enable wg-quick@wg1
sudo systemctl start wg-quick@wg1
sudo hostname gwrd
hostname | sudo tee /etc/hostname
sudo sed -i -e "s/gw/gwrd/" /etc/hosts


# KHzd0OF4CfTl0gyK1Pz7j/nDrQbyxrLqK/8KWgdAfX0=
# 5m8Fitj/sUxdcctnGs/V1RMelS2Vc1cV1mNAlGmYBW4=

