#!/bin/bash
for i in `find * | grep lab | grep yaml` 
do 
  password=`cat $i | grep adpassword`
  if [ "${password}" ]
  then
        echo "filename $i"
        echo "Password ${password}"
  	sed -i .bak -e 's/MyPassword/AnaMabokCoy/' ${i}
	rm ${i}.bak
  fi
done
