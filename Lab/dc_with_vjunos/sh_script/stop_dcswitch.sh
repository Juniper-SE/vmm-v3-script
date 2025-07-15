#!/bin/bash
for i in dc1spine{1..4} dc1leaf{1..8} dc2sw{1..2}
do
  echo "vmm stop ${i}"
  echo "vmm unbind ${i}"
  echo "vmm bind ${i}"
done

for i in dc1spine{1..4} dc1leaf{1..8} dc2sw{1..2}
do
  echo "vmm start ${i}"
done
