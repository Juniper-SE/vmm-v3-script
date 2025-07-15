#!/usr/bin/env python3
from jnpr.junos import Device
from lxml import etree

with Device(host='pe1') as dev:
    data = dev.rpc.get_config()
    print (etree.tostring(data, encoding='unicode', pretty_print=True))

