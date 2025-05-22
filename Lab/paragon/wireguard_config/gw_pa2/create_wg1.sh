cat << EOF | sudo tee /etc/wireguard/wg1.conf
[Interface]
PrivateKey=GNjm2RWOeRNmuF3unzvT1sS8eVyaJhiqwEEGOJGSVW8=
Address=192.168.198.0/31
ListenPort=17845
[Peer]
PublicKey=8nP5vF12LMDiigXUnz0QgluliMKc8t9moEvoPZs7YUg=
AllowedIPs=192.168.198.1/32,10.100.0.0/16,172.16.10.0/24,192.168.255.0/24,172.16.14.0/24
# GNjm2RWOeRNmuF3unzvT1sS8eVyaJhiqwEEGOJGSVW8=
# IeMMC2xuVWIlspqnuoSMKdG3CCZ1+3O2KMzi+CSSXg0=
EOF
sudo systemctl enable wg-quick@wg1
sudo systemctl start wg-quick@wg1




cat << EOF | sudo tee /etc/wireguard/wg0.conf
[Interface]
PrivateKey=GNjm2RWOeRNmuF3unzvT1sS8eVyaJhiqwEEGOJGSVW8=
Address=192.168.197.0/31
ListenPort=17845
[Peer]
PublicKey=8nP5vF12LMDiigXUnz0QgluliMKc8t9moEvoPZs7YUg=
AllowedIPs=192.168.197.1/32
EOF


cat << EOF | sudo tee /usr/local/etc/wireguard/wg0home.conf
[Interface]
PrivateKey=6ItXfnOn3VQNuGOvRxpVrEkZIY/Am8u2hm7KKOCP+UU=
Address=192.168.197.1/31
[Peer]
PublicKey=IeMMC2xuVWIlspqnuoSMKdG3CCZ1+3O2KMzi+CSSXg0=
EndPoint=[2001:448a:2020:1412:9b3:7195:5bca:10]:17845
AllowedIPs=192.168.197.0/31,192.168.110.0/24,192.168.120.0/24
EOF