#!/bin/bash
scp ./install_desktop.sh desktop:~/
for i in svr4 svr8 svr9
do
  scp ./install_lxd.sh ${i}:~/
done
