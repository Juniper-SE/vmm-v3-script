#!/usr/bin/env python3
# to set and delete  route target, router_external status, floating ip pools and ipam

import cn_lib
#from vnc_api import vnc_api

host_api='http://127.0.0.1:8082'
vn =['vn-left','vn-right']
project_name='k8s-lab4'
workload_name = 'csrx4'
x=cn_lib.create_port_tuple(vn,workload_name,project_name,host_api)
print(x)