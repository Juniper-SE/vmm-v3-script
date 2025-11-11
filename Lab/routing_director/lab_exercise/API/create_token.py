#!/usr/bin/env python3
import requests, os, json

RD_IP=os.getenv('RD_IP')
RD_USER=os.getenv('RD_USER')
RD_PASSWD=os.getenv('RD_PASSWD')
if not RD_IP:
    print("RD_IP is not defined")
    exit()
if not RD_USER:
    print("RD_USER is not defined")
    exit()
if not RD_PASSWD:
    print("RD_PASSWD is not defined")
    exit()
login_id={"email" : RD_USER,"password":RD_PASSWD}
# API_EP="/api/v1/login"
# API_EP="/api/v1/orgs/stats"
API_EP="/api/v1/self/apitokens"
url = f"https://{RD_IP}{API_EP}"
print(f"URL {url}")
print(f" LOGIN ID {login_id}")
x = requests.post(url,auth=(RD_USER,RD_PASSWD),verify=False)
result = json.loads(x.text)
token_id = result['id']
token_key = result['key']
print(f"token ID {token_id}")
print(f"token key {token_key}")
txt1=f"""#!/usr/bin/env bash
export TOKEN_ID={token_id}
export TOKEN_API={token_key}
"""
with open("token.sh","w") as f1:
    f1.write(txt1)
print("writing token file")

