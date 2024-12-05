#!/usr/bin/env python3
from aos.sdk.client import Client
import urllib3

urllib3.disable_warnings()

client = Client("https://172.16.55.1/api",verify_certificates=False)
print(client.version.get())
