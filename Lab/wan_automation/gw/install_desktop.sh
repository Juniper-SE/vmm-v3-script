yum -y install epel-release
yum -y update
yum  -y groupinstall "GNOME Desktop" 
ln -sf /lib/systemd/system/runlevel5.target /etc/systemd/system/default.target
reboot
