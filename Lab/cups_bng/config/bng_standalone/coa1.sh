#!/bin/bash
echo User-Name="cpe1",Acct-Session-Id="313350", ERX-IPv4-Input-Service-Filter = "allow", ERX-IPv6-Input-Service-Filter = "allowv6"  | radclient -x 172.16.12.1 coa pass01



# get acctsessionid

select acctsessionid from radacct where username='cpe1' and acctstoptime is NULL;


#!/bin/bash
echo User-Name="cpe1",Acct-Session-Id="54", ERX-IPv4-Input-Service-Filter = "sf1", ERX-IPv6-Input-Service-Filter = "sf1v6"  | radclient -x 172.16.12.1 coa pass01
