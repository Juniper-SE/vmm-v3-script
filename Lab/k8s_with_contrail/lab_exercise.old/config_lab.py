#!/usr/bin/env python3
# to set route target, router_external status, and floating ip pools
import labk8s
import sys
d1=labk8s.check_arg(sys.argv)
if d1:
    if d1['command'] == 'set_rt':
        labk8s.set_rt_fip(d1)
    elif d1['command'] == 'del_rt':
        labk8s.del_rt_fip(d1)
    elif d1['command'] == 'del_ipam':
        labk8s.del_ipam(d1)
else:
    print("It just fail")
