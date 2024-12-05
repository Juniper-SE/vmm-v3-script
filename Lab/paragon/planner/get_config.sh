#!/bin/bash
for i in cx{1..2} cy{1..2} cz{1..2} ci{1..2}
do
    echo "retrieve configuration ${i}"
    ssh $i "show config" > ${i}.conf
done
for i in pex{1..6} pez{1..6} pey{1..4} pei{1..2}
do
    echo "retrieve configuration ${i}"
    ssh $i "show config" > ${i}.conf
done
