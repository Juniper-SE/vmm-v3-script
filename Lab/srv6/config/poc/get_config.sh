#!/bin/bash
for i in pe1{1..5} p{1..4}
do
	ssh $i "show configuration | display set | no-more " | tee v6/${i}.set
done
ssh crpd "sudo podman exec -it crpd cli -c 'show configuration | display set| no-more'" | tee v6/crpd.set
