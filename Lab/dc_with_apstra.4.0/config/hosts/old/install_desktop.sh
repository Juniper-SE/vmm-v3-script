# yum -y install epel-release
# yum -y update
# yum  -y groupinstall "GNOME Desktop" 
# ln -sf /lib/systemd/system/runlevel5.target /etc/systemd/system/default.target
apt -y update
apt -y upgrade
apt -y install lightdm xfce4 firefox

echo "[SeatDefaults]" >> /etc/lightdm/lightdm.conf
echo "allow-guest=false" >> /etc/lightdm/lightdm.conf
echo "user-session=xfce" >> /etc/lightdm/lightdm.conf

reboot
