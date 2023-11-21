#!/usr/bin/env python3
# to set and delete  route target, router_external status, floating ip pools and ipam

import requests, os, yaml
#from vnc_api import vnc_api

host_api='http://127.0.0.1:8082'
prefix = 'service-templates'
URL="{}/{}".format(host_api,prefix)
vn_list=requests.get(URL).json()
print(vn_list)
print(type(vn_list[prefix]))
for i in vn_list[prefix]:
    print(i)
