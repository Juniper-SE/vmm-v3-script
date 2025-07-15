#!/usr/bin/env python3
from aos.sdk.client import Client
import aos.sdk.generator as aos_gen
import json
from pprint import pprint

## Hide SSL warnings resulting from setting verify_certificates to True.
import urllib3

urllib3.disable_warnings()

client = None


def login(_username, _password, _base_url):
    """
    Log in to the Apstra server and create a client instance.
    """
    # pylint: disable=global-statement
    global client
    try:
        client = Client(_base_url, verify_certificates=False)
        client.login(_username, _password)
        print("Successfully logged in to Apstra server.")
        return client
    except Exception as e:
        print(f"Failed to log in: {str(e)}")
        return None
    
    
def generate_logical_device(ld1):
    """
    Generate a new logical device using the AOS-SDK.
    """
    try:
        logical_device_data = aos_gen.gen_logical_device(
            name=ld1['name'],
            panels=ld1['panel'],
        )
        logical_device_id = client.logical_devices.create(data=logical_device_data)
        print(
            "Successfully created logical device with ID: %s",
            logical_device_id['id']
        )
        return logical_device_id
    except Exception as e:
        print(f"Failed to generate logical device: {str(e)}")
        return None


username = "admin"
password = "J4k4rt4#01"
base_url = "https://172.16.55.1/api"

client=login(username,password,base_url)
ld1 = { 'name':'_SDK-48x10_6x100', 
       'panel' : [
                [
                    (
                        48,
                        10,
                        ["generic", "superspine", "access", "leaf", "spine", "peer"],
                    )
                ],
                [
                    (
                        6,
                        100,
                        ["generic", "superspine", "access", "leaf", "spine", "peer"],
                    )
                ],
            ]
       }
generate_logical_device(ld1)
ld1 = { 'name':'_AOS-10x1', 
       'panel' : [
                [
                    (
                        10,
                        1,
                        ["generic", "superspine", "access", "leaf", "spine", "peer"],
                    )
                ]
            ]
       }
generate_logical_device(ld1)
