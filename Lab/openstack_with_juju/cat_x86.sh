cat << EOF | sudo tee /etc/modprobe.d/qemu-system-x86.conf
options kvm-intel nested=y enable_apicv=n pml=n
EOF
