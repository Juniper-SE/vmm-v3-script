#!/bin/bash
for i in node{0..3} control desktop c1
do
ssh ${i} "sudo reboot"
done
