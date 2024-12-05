#!/bin/bash
username='admin'
password='^J4k4rt4#010507$'
NS='172.16.11.50'
PORT=443
REQB="{ \"user\" :
	{
	  \"domain\": \"spdomain\",
	  \"name\" : \"admin\"
	},
	\"password\":\"^J4k4rt4#010507$\",
	\"methods\" : [\"PASSWORD\"]
      }"
echo  $REQB
curl -u ${username}:${password} -X POST  -k -H "Content-Type: application/json" -d "${REQB}" https://${NS}:${PORT}/iam/authenticate
