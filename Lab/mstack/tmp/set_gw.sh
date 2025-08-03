#!/bin/bash
cat << EOF  | sudo tee /etc/dhcp/dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
option space NEW_OP;
option NEW_OP.image-file-name code 0 = text;
option NEW_OP.config-file-name code 1 = text;
option NEW_OP.image-file-type code 2 = text; 
option NEW_OP.transfer-mode code 3 = text;
option NEW_OP.alt-image-file-name code 4= text;
option NEW_OP.http-port code 5= text;
option NEW_OP-encapsulation code 43 = encapsulate NEW_OP;
option NEW_OP.proxyv4-info code 8 = text;
option option-150 code 150 = { ip-address };
option domain-name-servers 10.49.32.95, 10.49.32.97;


host lxc {
    hardware ethernet 56:04:17:00:2f:0d;
    fixed-address 172.16.11.101;
    option NEW_OP.config-file-name "lxc.conf";
    option host-name "lxc";
}
host node1 {
    hardware ethernet 56:04:17:00:2f:0b;
    fixed-address 172.16.11.111;
    option NEW_OP.config-file-name "node1.conf";
    option host-name "node1";
}
host node2 {
    hardware ethernet 56:04:17:00:2f:09;
    fixed-address 172.16.11.112;
    option NEW_OP.config-file-name "node2.conf";
    option host-name "node2";
}
host node3 {
    hardware ethernet 56:04:17:00:2f:07;
    fixed-address 172.16.11.113;
    option NEW_OP.config-file-name "node3.conf";
    option host-name "node3";
}
host node4 {
    hardware ethernet 56:04:17:00:2f:05;
    fixed-address 172.16.11.114;
    option NEW_OP.config-file-name "node4.conf";
    option host-name "node4";
}
host node5 {
    hardware ethernet 56:04:17:00:2f:03;
    fixed-address 172.16.11.115;
    option NEW_OP.config-file-name "node5.conf";
    option host-name "node5";
}
host sw1 {
    hardware ethernet 56:04:17:00:2e:fc;
    fixed-address 172.16.11.120;
    option NEW_OP.config-file-name "sw1.conf";
    option host-name "sw1";
}
subnet 172.16.11.0 netmask 255.255.255.0  {
    range 172.16.11.100 172.16.11.254;
    option routers 172.16.11.1;
    option option-150 172.16.11.1;
}
EOF
cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  ethernets:
    eth1:
      addresses : ['172.16.11.1/24']
       
    eth2:
      addresses : ['172.16.12.0/31', 'fc00:dead:beef:a012::0/127']
      routes: 
       - to: 172.16.101.0/24
         via: 172.16.12.1
         metric: 1
       - to: 172.16.102.0/24
         via: 172.16.12.1
         metric: 1
       - to: 172.16.103.0/24
         via: 172.16.12.1
         metric: 1
       - to: 172.16.104.0/24
         via: 172.16.12.1
         metric: 1
       - to: fc00:dead:beef:a101::/64
         via: fc00:dead:beef:a012::1
         metric: 1
       - to: fc00:dead:beef:a102::/64
         via: fc00:dead:beef:a012::1
         metric: 1
       - to: fc00:dead:beef:a103::/64
         via: fc00:dead:beef:a012::1
         metric: 1
       - to: fc00:dead:beef:a104::/64
         via: fc00:dead:beef:a012::1
         metric: 1
       
       
    eth3:
      addresses : ['172.16.13.1/24', 'fc00:dead:beef:a013::1/64']
       
      
EOF



cat << EOF | sudo tee /usr/local/bin/start_vnc.sh
#!/bin/bash
websockify -D --web=/usr/share/novnc/ 6081 q-pod-67w.englab.juniper.net:5902
websockify -D --web=/usr/share/novnc/ 6082 q-pod-67t.englab.juniper.net:5902
websockify -D --web=/usr/share/novnc/ 6083 q-pod-68j.englab.juniper.net:5901
websockify -D --web=/usr/share/novnc/ 6084 q-pod-67g.englab.juniper.net:5903
websockify -D --web=/usr/share/novnc/ 6085 q-pod-68r.englab.juniper.net:5902
websockify -D --web=/usr/share/novnc/ 6086 q-pod-68i.englab.juniper.net:5905
exit 1
EOF

sudo chmod +x /usr/local/bin/start_vnc.sh

cat << EOF | sudo tee /etc/update-motd.d/99-update
#!/bin/bash
echo "----------------------------------------------"
echo "To access console of VM, use the following URL"
echo "----------------------------------------------"
echo "console lxc : http://10.51.134.27:6081/vnc.html"
echo "console node1 : http://10.51.134.27:6082/vnc.html"
echo "console node2 : http://10.51.134.27:6083/vnc.html"
echo "console node3 : http://10.51.134.27:6084/vnc.html"
echo "console node4 : http://10.51.134.27:6085/vnc.html"
echo "console node5 : http://10.51.134.27:6086/vnc.html"
EOF

sudo chmod +x  /etc/update-motd.d/99-update
cat << EOF | tee ~/.ssh/authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDBUA+4YJwqE2rqwweZ3NG7GpXF3JqIxFbnDxraW8//QWjHLGVgn+jFbXFB3T/yLYpIRAh8SsAw6M6pZXzGd3oiltENLkoN5YGI1yW0bCTsS/Z4BoW/iuPR2rYQqhA+NPi9OZO/opVbJ+VIdfm+fugWPSVpduBiJN20P9iEF1zCW4EmWZn3qkl25LjVSBVMiwn+crcsCHUub3xDRicgTOOINFo4lZy03Fsa3PoqpxXv18FhNi3pVWmV2n3vIckWt8BbaPWMTFZmERHkVb4Y15GsHwcQxb6gm3h8Do4QgURbujCUJQhpJT4BRdD8kja1NQK4lbcPq6l9rF3YM7aQkscB16nCplWcgdnxI7eN//FA4ovvx7d57i43Y7GzSlQE87kcIDDQ1eCesYOfg9EfqCFSVWV0hbhc2Ap6YCoc0R9POpG1n0LO+o++h0J0bkLUWsIiQLb3LiC91FnP3giK5MEzdJ+maJcjIyGlTth52s01nLdT4gQDgTURqIpfL8L0HWE= irzan@irzan-mbp
EOF

cat << EOF |  tee ~/.ssh/id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
EOF

chmod og-rwx ~/.ssh/*

sudo netplan apply

sudo systemctl enable startup.service
sudo systemctl restart startup.service
sudo systemctl restart isc-dhcp-server
sudo systemctl restart tftpd-hpa
sudo mv ~/tftp/*.conf /srv/tftp/
# sudo reboot
