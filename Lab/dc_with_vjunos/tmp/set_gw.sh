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


host vxlangw {
    hardware ethernet 56:04:1a:00:3c:da;
    fixed-address 172.16.10.213;
    option NEW_OP.config-file-name "vxlangw.conf";
    option host-name "vxlangw";
}
host pe1 {
    hardware ethernet 56:04:1a:00:3a:69;
    fixed-address 172.16.10.204;
    option NEW_OP.config-file-name "pe1.conf";
    option host-name "pe1";
}
host pe2 {
    hardware ethernet 56:04:1a:00:39:cc;
    fixed-address 172.16.10.205;
    option NEW_OP.config-file-name "pe2.conf";
    option host-name "pe2";
}
host pe3 {
    hardware ethernet 56:04:1a:00:59:2a;
    fixed-address 172.16.10.206;
    option NEW_OP.config-file-name "pe3.conf";
    option host-name "pe3";
}
host p1 {
    hardware ethernet 56:04:1a:00:39:d3;
    fixed-address 172.16.10.208;
    option NEW_OP.config-file-name "p1.conf";
    option host-name "p1";
}
host apstra {
    hardware ethernet 56:04:1a:00:3a:71;
    fixed-address 172.16.55.1;
    option NEW_OP.config-file-name "apstra.conf";
    option host-name "apstra";
}
host apstraw2 {
    hardware ethernet 56:04:1a:00:3a:cb;
    fixed-address 172.16.55.2;
    option NEW_OP.config-file-name "apstraw2.conf";
    option host-name "apstraw2";
}
host apstraw3 {
    hardware ethernet 56:04:1a:00:3a:16;
    fixed-address 172.16.55.3;
    option NEW_OP.config-file-name "apstraw3.conf";
    option host-name "apstraw3";
}
host ztp {
    hardware ethernet 56:04:1a:00:39:ec;
    fixed-address 172.16.55.4;
    option NEW_OP.config-file-name "ztp.conf";
    option host-name "ztp";
}
host flow {
    hardware ethernet 56:04:1a:00:60:c6;
    fixed-address 172.16.55.5;
    option NEW_OP.config-file-name "flow.conf";
    option host-name "flow";
}
host kvm1 {
    hardware ethernet 56:04:1a:00:3a:77;
    fixed-address 172.16.10.221;
    option NEW_OP.config-file-name "kvm1.conf";
    option host-name "kvm1";
}
host kvm2 {
    hardware ethernet 56:04:1a:00:3b:d3;
    fixed-address 172.16.10.222;
    option NEW_OP.config-file-name "kvm2.conf";
    option host-name "kvm2";
}
host kvm3 {
    hardware ethernet 56:04:1a:00:59:0a;
    fixed-address 172.16.10.223;
    option NEW_OP.config-file-name "kvm3.conf";
    option host-name "kvm3";
}
host kvm4 {
    hardware ethernet 56:04:1a:00:3a:75;
    fixed-address 172.16.10.224;
    option NEW_OP.config-file-name "kvm4.conf";
    option host-name "kvm4";
}
host kvm5 {
    hardware ethernet 56:04:1a:00:4f:6e;
    fixed-address 172.16.10.225;
    option NEW_OP.config-file-name "kvm5.conf";
    option host-name "kvm5";
}
host kvm6 {
    hardware ethernet 56:04:1a:00:3a:cc;
    fixed-address 172.16.10.226;
    option NEW_OP.config-file-name "kvm6.conf";
    option host-name "kvm6";
}
host kvm7 {
    hardware ethernet 56:04:1a:00:3a:93;
    fixed-address 172.16.10.230;
    option NEW_OP.config-file-name "kvm7.conf";
    option host-name "kvm7";
}
subnet 172.16.10.0 netmask 255.255.255.0  {
    range 172.16.10.1 172.16.10.200;
    option routers 172.16.10.254;
    option option-150 172.16.10.254;
}
subnet 172.16.55.0 netmask 255.255.255.0  {
    range 172.16.55.1 172.16.55.200;
    option routers 172.16.55.254;
    option option-150 172.16.55.254;
}
EOF
cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  ethernets:
    eth1:
      addresses : ['172.16.10.254/24']
       
    eth2:
      addresses : ['172.16.15.1/24', 'fc00:dead:beef:ff15::1/64']
       
    eth3:
      addresses : ['172.16.16.254/24', 'fc00:dead:beef:ff16::FFFF/64']
      mtu: 9000
       
    eth4:
      addresses : ['172.16.14.254/24', 'fc00:dead:beef:ff14::FFFF/64']
      mtu: 9000
      routes: 
       - to: 172.16.11.0/24
         via: 172.16.14.1
         metric: 1
       - to: 172.16.12.0/24
         via: 172.16.14.1
         metric: 1
       - to: 172.16.13.0/24
         via: 172.16.14.1
         metric: 1
       - to: fc00:dead:beef:ff11::/64
         via: fc00:dead:beef:ff14::1
         metric: 1
       - to: fc00:dead:beef:ff12::/64
         via: fc00:dead:beef:ff14::1
         metric: 1
       - to: fc00:dead:beef:ff13::/64
         via: fc00:dead:beef:ff14::1
         metric: 1
       
       
    eth5:
      addresses : ['172.16.55.254/24', 'fc00:dead:beef:ff55::FFFF/64']
      mtu: 9000
       
      
EOF



cat << EOF | sudo tee /usr/local/bin/start_vnc.sh
#!/bin/bash
websockify -D --web=/usr/share/novnc/ 6081 q-pod-76d.englab.juniper.net:5905
websockify -D --web=/usr/share/novnc/ 6082 q-pod-76e.englab.juniper.net:5912
websockify -D --web=/usr/share/novnc/ 6083 q-pod-76w.englab.juniper.net:5909
websockify -D --web=/usr/share/novnc/ 6084 q-pod-77r.englab.juniper.net:5904
websockify -D --web=/usr/share/novnc/ 6085 q-pod-76s.englab.juniper.net:5906
websockify -D --web=/usr/share/novnc/ 6086 q-pod-77p.englab.juniper.net:5905
websockify -D --web=/usr/share/novnc/ 6087 q-pod-77j.englab.juniper.net:5907
websockify -D --web=/usr/share/novnc/ 6088 q-pod-77b.englab.juniper.net:5908
websockify -D --web=/usr/share/novnc/ 6089 q-pod-76q.englab.juniper.net:5906
websockify -D --web=/usr/share/novnc/ 6090 q-pod-76c.englab.juniper.net:5908
websockify -D --web=/usr/share/novnc/ 6091 q-pod-77g.englab.juniper.net:5908
websockify -D --web=/usr/share/novnc/ 6092 q-pod-77d.englab.juniper.net:5909
websockify -D --web=/usr/share/novnc/ 6093 q-pod-77w.englab.juniper.net:5903
websockify -D --web=/usr/share/novnc/ 6094 q-pod-76a.englab.juniper.net:5906
websockify -D --web=/usr/share/novnc/ 6095 q-pod-77m.englab.juniper.net:5907
websockify -D --web=/usr/share/novnc/ 6096 q-pod-77h.englab.juniper.net:5906
websockify -D --web=/usr/share/novnc/ 6097 q-pod-76k.englab.juniper.net:5906
websockify -D --web=/usr/share/novnc/ 6098 q-pod-77s.englab.juniper.net:5909
websockify -D --web=/usr/share/novnc/ 6099 q-pod-77l.englab.juniper.net:5902
websockify -D --web=/usr/share/novnc/ 6100 q-pod-77e.englab.juniper.net:5905
websockify -D --web=/usr/share/novnc/ 6101 q-pod-76f.englab.juniper.net:5905
websockify -D --web=/usr/share/novnc/ 6102 q-pod-76e.englab.juniper.net:5911
websockify -D --web=/usr/share/novnc/ 6103 q-pod-76d.englab.juniper.net:5906
websockify -D --web=/usr/share/novnc/ 6104 q-pod-77d.englab.juniper.net:5908
exit 1
EOF

sudo chmod +x /usr/local/bin/start_vnc.sh

cat << EOF | sudo tee /etc/update-motd.d/99-update
#!/bin/bash
echo "----------------------------------------------"
echo "To access console of VM, use the following URL"
echo "----------------------------------------------"
echo "console apstra : http://10.49.10.204:6081/vnc.html"
echo "console apstraw2 : http://10.49.10.204:6082/vnc.html"
echo "console apstraw3 : http://10.49.10.204:6083/vnc.html"
echo "console ztp : http://10.49.10.204:6084/vnc.html"
echo "console flow : http://10.49.10.204:6085/vnc.html"
echo "console svr1a : http://10.49.10.204:6086/vnc.html"
echo "console svr1b : http://10.49.10.204:6087/vnc.html"
echo "console svr2 : http://10.49.10.204:6088/vnc.html"
echo "console svr3a : http://10.49.10.204:6089/vnc.html"
echo "console svr3b : http://10.49.10.204:6090/vnc.html"
echo "console svr4 : http://10.49.10.204:6091/vnc.html"
echo "console svr5 : http://10.49.10.204:6092/vnc.html"
echo "console svr6 : http://10.49.10.204:6093/vnc.html"
echo "console svr7 : http://10.49.10.204:6094/vnc.html"
echo "console kvm1 : http://10.49.10.204:6095/vnc.html"
echo "console kvm2 : http://10.49.10.204:6096/vnc.html"
echo "console kvm3 : http://10.49.10.204:6097/vnc.html"
echo "console kvm4 : http://10.49.10.204:6098/vnc.html"
echo "console svr8a : http://10.49.10.204:6099/vnc.html"
echo "console svr8b : http://10.49.10.204:6100/vnc.html"
echo "console svr9 : http://10.49.10.204:6101/vnc.html"
echo "console kvm5 : http://10.49.10.204:6102/vnc.html"
echo "console kvm6 : http://10.49.10.204:6103/vnc.html"
echo "console kvm7 : http://10.49.10.204:6104/vnc.html"
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
