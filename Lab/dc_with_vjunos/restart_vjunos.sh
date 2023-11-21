#!/bin/bash
for i in dc1spine{1..4}
do
  echo  vmm stop $i
  echo  vmm unbind $i
done
for i in dc1leaf{1..8}
do
   echo vmm stop $i
   echo vmm unbind $i
done
for i in dc2sw{1..2}
do
   echo vmm stop $i
   echo vmm unbind $i
done

for i in dc3spine{1..2}
do
   echo vmm stop $i
   echo vmm unbind $i
done
for i in dc3leaf{1..6}
do
   echo vmm stop $i
   echo vmm unbind $i
done

for i in dc1spine{1..4}
do
  echo  vmm bind $i
done
for i in dc1leaf{1..8}
do
  echo  vmm bind $i
done
for i in dc2sw{1..2}
do
  echo  vmm bind $i
done

for i in dc3spine{1..2}
do
   echo vmm bind $i
done
for i in dc3leaf{1..6}
do
   echo vmm bind $i
done
