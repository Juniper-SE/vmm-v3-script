#!/usr/bin/env python3
import apstra_api
# main program
asn=['ASN1','ASN2','ASN3']
for i in asn:
    print(f"delete ASN pool {i}")
    apstra_api.delete_asn_pools(i)