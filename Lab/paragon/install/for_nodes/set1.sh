echo "*         hard    nofile      1048576
*         soft    nofile      1048576
root      hard    nofile      1048576
root      soft    nofile      1048576
influxdb  hard    nofile      1048576
influxdb  soft    nofile      1048576" | sudo tee -a /etc/security/limits.conf

echo "fs.file-max = 2097152
vm.max_map_count=262144
fs.inotify.max_user_watches=524288
fs.inotify.max_user_instances=512" | sudo tee -a /etc/sysctl.conf

sudo sed -i -e 's/#AllowTcpForwarding/AllowTcpForwarding/' /etc/ssh/sshd_config


