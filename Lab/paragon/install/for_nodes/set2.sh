#!/bin/bash
sudo fdisk -l /dev/sda
echo "n
3


w
q
" | sudo fdisk /dev/sda
sudo fdisk -l /dev/sda
