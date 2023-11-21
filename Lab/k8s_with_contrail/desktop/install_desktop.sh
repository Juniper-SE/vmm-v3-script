sudo apt -y update
sudo apt -y upgrade
sudo apt -y install lightdm xfce4 firefox python3-pip

echo "[SeatDefaults]"  | sudo tee -a /etc/lightdm/lightdm.conf
echo "allow-guest=false" | sudo tee -a /etc/lightdm/lightdm.conf
echo "user-session=xfce" | sudo tee -a /etc/lightdm/lightdm.conf

sudo reboot
