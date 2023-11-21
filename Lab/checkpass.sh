for i in `find * | grep lab | grep yaml`
do 
  password=`cat $i | grep adpassword`
  if [ "${password}" ]
  then
  	echo "filename $i"
	echo "Password ${password}"
  fi
done
