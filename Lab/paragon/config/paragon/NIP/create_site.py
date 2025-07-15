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
with open("sites.yaml") as f1:
    new_site=yaml.load(f1,Loader=yaml.FullLoader)
# create new org
url = f"https://{pa_ip}/api/v1/orgs"
print(f"Creating organization {org_name}")
org_data={
    "allow_mist": True,
    "name": org_name
}
r=requests.post(url,verify=False,auth=login_id,json=org_data)
print(f"status {r.status_code}")
d1=json.loads(r.content)
org_id = d1['id']
print(f"organization {org_name}, ID {org_id}")
yaml_objects = yaml.dump(d1)
with open("org.yaml","w") as f1:
    f1.write(yaml_objects)

# Create new sites
url = f"https://{pa_ip}/api/v1/orgs/{org_id}/sites"
site_data={}
for i in new_site:
    print(f"Creating site {i['name']}")
    r=requests.post(url,verify=False,auth=login_id,json=i)
    print(f"status {r.status_code}")
    d1=json.loads(r.content)
    # print(f"content {d1}")
    print(f"{i['name']} : {d1['id']}")
    site_data[i['name']]=d1['id']
yaml_objects = yaml.dump(site_data)
with open("site_id.yaml","w") as f1:
    f1.write(yaml_objects)
