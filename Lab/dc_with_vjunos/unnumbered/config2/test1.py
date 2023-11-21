#!/usr/local/bin/python
from jnpr.junos import Device
from pprint import pprint

with Device(host='spine1') as dev:
    pprint (dev.facts['hostname'])
    pprint (dev.facts)
