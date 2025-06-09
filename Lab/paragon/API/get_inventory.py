#!/usr/bin/env python3
import requests
import json
import yaml
# variable
pa_ip='172.16.12.1'
email="irzan@juniper.net"
password="J4k4rt4#170845"
login_id=(email,password)
org_id="b7c3735e-35a1-425c-b5d8-7a0a8aa080c5"
url = f"https://{pa_ip}/api/v1/orgs/{org_id}/inventory"
r=requests.get(url,verify=False,auth=login_id)
print(f"status {r.status_code}")
d1=json.loads(r.content)
print(d1)
