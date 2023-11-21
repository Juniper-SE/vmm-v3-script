#!/usr/bin/env python3
# to set and delete  route target, router_external status, floating ip pools and ipam

import cn_lib
#from vnc_api import vnc_api

host_api='http://127.0.0.1:8082'
vn =['vn-left','vn-right']
ns = 'lab4'
cluster='k8s'
project_name="{}-{}".format(cluster,ns)
workload_name = 'csrx1'

for i in vn:
    href = cn_lib.get_vmi_href(i,workload_name,project_name,host_api)
    print("workload {}, vn {}, href {}".format(workload_name,i,href))
