#!/usr/bin/env bash
for i in 1 2 3 4
do
  echo "vmm stop dc1spine${i}"
  echo "vmm unbind dc1spine${i}"
done
for j in 1 2 3 4 5 6 7 8
do 
    echo "vmm stop dc1leaf${j}"
    echo "vmm unbind dc1leaf${j}"
done
for i in 1 2
do
echo "vmm stop dc2sw${i}"
echo "vmm unbind dc2sw${i}"
done
for i in 1 2 
do
 echo "vmm stop dc3spine${i}"
 echo "vmm unbind dc3spine${i}"
done
for j in 1 2 3 4 5 6 
do 
  echo "vmm stop dc3leaf${j}"
  echo "vmm unbind dc3leaf${j}"
done
