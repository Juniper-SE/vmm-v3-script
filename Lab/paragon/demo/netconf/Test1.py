#!/usr/bin/env python3
from pprint import pprint
from jnpr.junos import Device
dev = Device(host='pe1', user='admin', password='pass01')
dev.open()
pprint(dev.facts)
dev.close()
