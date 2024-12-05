#!/usr/bin/env python3
import requests
import urllib3
urllib3.disable_warnings()
APSTRA_IP='127.0.0.1:17845'
USERNAME='admin'
PASSWORD='J4k4rt4#01'
proxies={'http': 'socks5h://127.0.0.1:1080','https': 'socks5h://127.0.0.1:1080'}
#resp=requests.get('https://172.16.10.2/api/versions/server',proxies=proxies)
resp=requests.get(f"https://{APSTRA_IP}/api/versions/server",verify=False)
print("Response ",resp.status_code)
print("Response ",resp.json())
