#!/bin/bash
# for i in ctrl{1..3}
for i in node0
do
  scp answer.txt ${i}:~/
  ssh ${i} "cat ~/answer.txt | sudo lxd init; lxc profile show default; sleep 2; lxc profile set default security.nesting=true; lxc profile set default security.privileged=true"
done
