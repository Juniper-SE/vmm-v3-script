#!/bin/bash
USER="admin"
DESTD="hw_cli"
for i in cx{1..2} cy{1..2} cz{1..2} ci{1..2} pex{1..6} pez{1..6} pey{1..4} pei{1..2}
do
    echo "retrieve configuration ${i}"
    echo "${USER}@${i}> set cli screen-width 0" > ${DESTD}/${i}.equipment_cli
    echo "Screen width set to 0" >> ${DESTD}/${i}.equipment_cli
    echo " " >> ${DESTD}/${i}.equipment_cli
    echo "${USER}@${i}> show configuration system host-name | display inheritance" >> ${DESTD}/${i}.equipment_cli
    ssh ${USER}@${i} "show configuration system host-name | display inheritance" >> ${DESTD}/${i}.equipment_cli
    echo " " >> ${DESTD}/${i}.equipment_cli
    echo "${USER}@${i}> show version" >> ${DESTD}/${i}.equipment_cli
    ssh ${USER}@${i} "show version" >> ${DESTD}/${i}.equipment_cli
    echo " " >> ${DESTD}/${i}.equipment_cli
    echo "${USER}@${i}>  show chassis hardware" >> ${DESTD}/${i}.equipment_cli
    ssh ${USER}@${i} "show chassis hardware" >> ${DESTD}/${i}.equipment_cli
    echo " " >> ${DESTD}/${i}.equipment_cli
    echo  "${USER}@${i}> show chassis fpc" >> ${DESTD}/${i}.equipment_cli
    ssh ${USER}@${i} "show chassis fpc" >> ${DESTD}/${i}.equipment_cli
    echo " " >> ${DESTD}/${i}.equipment_cli
    echo "${USER}@${i}> show chassis hardware models" >> ${DESTD}/${i}.equipment_cli
    ssh ${USER}@${i} "show chassis hardware models" >> ${DESTD}/${i}.equipment_cli
    echo " " >> ${DESTD}/${i}.equipment_cli
done

