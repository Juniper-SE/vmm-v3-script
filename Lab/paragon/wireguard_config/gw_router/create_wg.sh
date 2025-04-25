cat << EOF | sudo tee /etc/wireguard/wg0.conf
[Interface]
PrivateKey=6ItXfnOn3VQNuGOvRxpVrEkZIY/Am8u2hm7KKOCP+UU=
Address=192.168.198.1/31
[Peer]
PublicKey=IeMMC2xuVWIlspqnuoSMKdG3CCZ1+3O2KMzi+CSSXg0=
EndPoint=10.56.11.69:17845
AllowedIPs=192.168.198.0/32,172.16.11.0/24,172.16.12.0/24
# 6ItXfnOn3VQNuGOvRxpVrEkZIY/Am8u2hm7KKOCP+UU=
# 8nP5vF12LMDiigXUnz0QgluliMKc8t9moEvoPZs7YUg=
EOF

sudo systemctl enable wg-quick@wg0

sudo systemctl start wg-quick@wg0

sudo hostname gwpa2net
hostname | sudo tee /etc/hostname



