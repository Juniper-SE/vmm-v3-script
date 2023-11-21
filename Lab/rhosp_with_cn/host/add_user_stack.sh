useradd stack
#passwd stack
echo "stack ALL=(root) NOPASSWD:ALL" | tee -a /etc/sudoers.d/stack
chmod 0440 /etc/sudoers.d/stack
cat << EOF | tee /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
172.16.11.9 director.vmmlab.com director
172.16.12.9 director.vmmlab.com director
172.16.12.10 os0.vmmlab.com os0
172.16.12.11 cc0.vmmlab.com cc0
172.16.12.12 cadb0.vmmlab.com cadb0
172.16.12.13 can0.vmmlab.com can0
172.16.12.20 compute0.vmmlab.com compute0
172.16.12.21 compute1.vmmlab.com compute1
172.16.12.22 compute2.vmmlab.com compute2
EOF

mkdir /home/stack/.ssh
cp /home/rhel/keylab /home/stack/.ssh/id_rsa
cp /home/rhel/keylab.pub /home/stack/.ssh/authorized_keys
cp /home/rhel/keylab.pub /home/stack/.ssh/id_rsa.pub
chown -R stack:stack /home/stack/.ssh
chmod -R og-rwx /home/stack/.ssh
