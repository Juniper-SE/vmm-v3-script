#!/usr/bin/env python3
import apstra_api
import sys
# main program
if len(sys.argv) != 2:
    print("what is the device profile name ?")
else:
    deviceprofile=sys.argv[1]
    id=apstra_api.get_id_device_profiles(deviceprofile)
    print(f"device profile {deviceprofile}: id {id}")