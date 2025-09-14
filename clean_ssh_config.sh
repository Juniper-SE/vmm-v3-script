#!/bin/bash
LINENUM=`grep -n '###' ~/.ssh/config | cut -d ':' -f 1`
if [ -z "${LINENUM}" ];
then
	echo "nothing on the config"
else
	echo "deleting config, from line ${LINENUM} to the end"
	sed -i -e "${LINENUM},\$d" ~/.ssh/config
fi
