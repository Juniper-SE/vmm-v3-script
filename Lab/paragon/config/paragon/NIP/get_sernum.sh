#/usr/bin/env bash
echo "---" | tee sernum.yaml
for i in pe{1..4} p{1..5}
do
   SERNUM=`ssh admin@${i} "show chassis hardware | match Chassis" | tr -s " " | cut -d " " -f 2`
   echo "${i} : ${SERNUM}" | tee -a sernum.yaml
done
