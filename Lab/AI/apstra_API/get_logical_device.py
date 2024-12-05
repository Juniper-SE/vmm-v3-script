#!/usr/bin/env python3
import apstra_api
import sys
# main program
if len(sys.argv) != 2:
    print("what is the logical device name ?")
else:
    logicaldevice=sys.argv[1]
    id=apstra_api.get_id_logical_devices(logicaldevice)
    print(f"device profile {logicaldevice}: id {id}")