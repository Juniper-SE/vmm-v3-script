#!/usr/bin/env python3
import requests, os, json

import requests, json, os
RD_IP=os.getenv('RD_IP')
TOKEN_API=os.getenv('TOKEN_API')
ORG_NAME=os.getenv('ORG_NAME')
if not RD_IP:
    print("RD_IP is not defined")
    exit()
if not TOKEN_API:
    print("TOKEN_API is not defined")
    exit()
if not ORG_NAME:
    print("ORG_NAME is not defined")
    exit()

API_EP="/api/v1/orgs"
url = f"https://{RD_IP}{API_EP}"
data1={ "allow_mist": True,
"name": ORG_NAME
}
headers={'Authorization':f"Token {TOKEN_API}"}
print(f"URL {url}")
x = requests.post(url,headers=headers,json=data1,verify=False)
print(x.text)
x2 = json.loads(x.text)
org_name=x2['name']
org_id=x2['id']

print(f"ORG Name {org_name}")
print(f"ORGD ID {org_id}")
txt1=f"""#!/usr/bin/env bash
export ORG_ID={org_id}
export ORG_NAME={org_name}
"""
with open("org.sh","w") as f1:
    f1.write(txt1)
print("writing org file")