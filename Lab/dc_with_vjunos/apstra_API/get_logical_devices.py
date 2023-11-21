#!/usr/bin/env python3
import apstra_api
import yaml
# main program
#apstra_api.get_list_logical_devices()
ld_name = [ 'vEX_Spine','vEX_Leaf', 'vEX_Collapsed']
#id = apstra_api.get_id_logical_devices(ld_name)
#print(f"logical devices {ld_name} : ID {id}")
for i in ld_name:
    ld=apstra_api.get_logical_devices(i)
    print(f"logical devices {i}")
    print(yaml.dump(ld))
