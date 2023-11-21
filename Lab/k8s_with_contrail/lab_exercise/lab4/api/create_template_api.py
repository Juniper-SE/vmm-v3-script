#!/usr/bin/env python3

import requests, os, yaml

host='127.0.0.1'
object='service-templates'
url="http://{}:8082/{}".format(host,object)
#r=requests.get(url)
st_name = 'fw1'
service_mode = "in-network"
service_type = "firewall"
d1 = {
    "service-template": {
        "fq_name": ["default-domain",st_name],
        "parent_type": "domain",
        "service_template_properties": {
            "service_virtualization_type": "virtual-machine",
            "interface_type": [
                {
                    "service_interface_type": "left"
                },
                {
                    "service_interface_type": "right"
                }
            ],
            "service_mode": service_mode,
            "version": 2,
            "service_type": service_type
        }
    }
}
#print(url)
#print(d1)
r=requests.post(url,json=d1)
print("status ",r.status_code)
#print('result ',r.text)
#print('result json ',r.json())

