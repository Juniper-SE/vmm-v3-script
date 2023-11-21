#!/bin/bash
sudo sed -i -e '/GRUB_DEFAULT/ d' /etc/default/grub
echo "GRUB_DEFAULT=0" | sudo tee -a /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg