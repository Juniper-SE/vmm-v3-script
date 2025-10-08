cat << EOF | sudo tee /etc/wireguard/wg1.conf
[Interface]
PrivateKey=KHzd0OF4CfTl0gyK1Pz7j/nDrQbyxrLqK/8KWgdAfX0=
Address=192.168.199.2/31
ListenPort=17845
[Peer]
# gwnet
PublicKey=cdOoPi0T/PyjCkgSynB4K/3+ta5Ryox0DkmK9UQLrVI=
AllowedIPs=192.168.199.3/32,172.16.51.0/24,172.16.52.0/24

EOF
sudo systemctl enable wg-quick@wg1
sudo systemctl start wg-quick@wg1
sudo hostname gwapstra
hostname | sudo tee /etc/hostname
sudo sed -i -e "s/gw/gwapstra/" /etc/hosts


# KHzd0OF4CfTl0gyK1Pz7j/nDrQbyxrLqK/8KWgdAfX0=
# 5m8Fitj/sUxdcctnGs/V1RMelS2Vc1cV1mNAlGmYBW4=

