#!/usr/bin/env python3
import apstra_api
import sys
# main program
if len(sys.argv) != 2:
    print("what is the rack_type name ?")
else:
    rack_name=sys.argv[1]
    id=apstra_api.get_id_rack_type(rack_name)
    print(f"rack name {rack_name}: id {id}")