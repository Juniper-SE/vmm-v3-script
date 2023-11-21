#!/usr/bin/env python3
from pprint import pprint
from jnpr.junos import Device
sshkeyfile='./key1.pem'
host='pe1'
user='admin'
dev = Device(host=host, user=user,ssh_private_key_file=sshkeyfile)
dev.open()
pprint(dev.facts)
dev.close()
