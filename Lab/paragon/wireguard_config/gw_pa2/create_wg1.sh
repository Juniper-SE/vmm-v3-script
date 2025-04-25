cat << EOF | sudo tee /etc/wireguard/wg1.conf
[Interface]
PrivateKey=GNjm2RWOeRNmuF3unzvT1sS8eVyaJhiqwEEGOJGSVW8=
Address=192.168.198.0/31
ListenPort=17845
[Peer]
PublicKey=8nP5vF12LMDiigXUnz0QgluliMKc8t9moEvoPZs7YUg=
AllowedIPs=192.168.198.1/32,10.100.2.0/24,172.16.10.0/24,192.168.255.0/24,10.1.0.0/16,172.16.14.0/24
# GNjm2RWOeRNmuF3unzvT1sS8eVyaJhiqwEEGOJGSVW8=
# IeMMC2xuVWIlspqnuoSMKdG3CCZ1+3O2KMzi+CSSXg0=
EOF
sudo systemctl enable wg-quick@wg1
sudo systemctl start wg-quick@wg1

