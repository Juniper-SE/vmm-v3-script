#!/usr/bin/env python3
import requests, os, json

import requests, json, os
RD_IP=os.getenv('RD_IP')
RD_USER=os.getenv('RD_USER')
RD_PASSWD=os.getenv('RD_PASSWD')
TOKEN_API=os.getenv('TOKEN_API')
ORG_ID=os.getenv('ORG_ID')
if not RD_IP:
    print("RD_IP is not defined")
    exit()
# if not TOKEN_API:
#     print("TOKEN_API is not defined")
#     exit()
if not ORG_ID:
    print("ORG_ID is not defined")
    exit()
if not RD_USER:
    print("RD_USER is not defined")
    exit()
if not RD_PASSWD:
    print("RD_PASSWD is not defined")
    exit()
login_id={"email" : RD_USER,"password":RD_PASSWD}
API_EP=f"/api/v1/orgs/{ORG_ID}"
url = f"https://{RD_IP}{API_EP}"
print(url)
data1={ "allow_mist": True,
"name": "jsi"
}
# headers={'Authorization':f"Token {TOKEN_API}"}
print(f"URL {url}")
x = requests.delete(url,auth=(RD_USER,RD_PASSWD),verify=False)
print(x.text)