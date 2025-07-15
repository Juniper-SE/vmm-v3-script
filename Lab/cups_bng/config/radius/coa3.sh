#!/bin/bash
echo User-Name="cpe1",Acct-Session-Id="54", ERX-Ingress-Policy-Name = "super", ERX-Egress-Policy-Name = "super", ERX-IPv6-Ingress-Policy-Name= "superv6", ERX-IPv6-Egress-Policy-Name="superv6"  | radclient -x 172.16.12.1 coa pass01
