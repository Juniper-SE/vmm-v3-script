#!/usr/bin/env python3
import requests
import json
import yaml
# variable
with open("paragon.yaml") as f1:
    pa_info=yaml.load(f1,Loader=yaml.FullLoader)
pa_ip=pa_info['pa_ip']
email=pa_info['email']
password=pa_info['password']
org_name = pa_info['org']
login_id=(email,password)
with open("org.yaml") as f1:
    org=yaml.load(f1,Loader=yaml.FullLoader)
org_id=org['id']
url = f"https://{pa_ip}/api/v1/orgs/{org_id}/ocdevices/outbound_ssh_cmd"
print("Getting outbound ssh command")
r=requests.get(url,verify=False,auth=login_id)
print(f"status {r.status_code}")
d1=json.loads(r.content)
with open("ocssh.set","w") as f1:
    f1.write(d1['cmd'])
