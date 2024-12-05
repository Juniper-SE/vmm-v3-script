#!/bin/bash
echo User-Name="cpe1",Acct-Session-Id="54", ERX-Ingress-Policy-Name = "police-10M", ERX-Egress-Policy-Name = "police-10M", ERX-IPv6-Ingress-Policy-Name= "police-10Mv6", ERX-IPv6-Egress-Policy-Name="police-10Mv6"  | radclient -x 172.16.12.1 coa pass01
