#!/bin/bash
date | tee -a /tmp/ssh_status.txt
RESULT=`ps -xa | grep "ssh -4 -R 62122:127.0.0.1:22" | grep Ss | tr -s " " | cut -f 2 -d ' '`
if [ $RESULT ] 
then	
echo "session is active" | tee -a /tmp/ssh_status.txt
else
echo "creating session PID $RESULT" | tee -a /tmp/ssh_status.txt
ssh -4 -R 62122:127.0.0.1:22 -p 443 -f -N -o ServerAliveInterval=3 irzan@debian1.irzan.com -i /home/ubuntu/.ssh/pchome.pem
fi
