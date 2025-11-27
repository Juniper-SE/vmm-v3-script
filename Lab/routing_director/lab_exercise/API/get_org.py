#!/usr/bin/env python3
import requests, os, json

import requests, json, os
RD_IP=os.getenv('RD_IP')
TOKEN_API=os.getenv('TOKEN_API')
ORG_ID=os.getenv('ORG_ID')
if not RD_IP:
    print("RD_IP is not defined")
    exit()
if not TOKEN_API:
    print("TOKEN_API is not defined")
    exit()
if not ORG_ID:
    print("ORG_NAME is not defined")
    exit()

API_EP=f"/api/v1/orgs/{ORG_ID}"
url = f"https://{RD_IP}{API_EP}"

headers={'Authorization':f"Token {TOKEN_API}"}
print(f"URL {url}")
x = requests.get(url,headers=headers,verify=False)
#print(x.text)
x2 = json.loads(x.text)
org_name=x2['name']
org_id=x2['id']

print(f"ORG Name {org_name}")
print(f"ORGD ID {org_id}")
