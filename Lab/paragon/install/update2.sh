#!/bin/bash
echo "Uploading to vm control"
scp ./install_docker.sh control:~/
# scp ./for_nodes/update_grub.sh control:~/
# ssh control "./update_grub.sh; sudo reboot"
for i in node{0..3}
do
	echo "Uploading to vm ${i}"
	scp ./for_nodes/*.sh ${i}:~/
	# ssh ${i} "chmod +x *.sh ; ~/set1.sh  ; ./set2.sh"
	# ssh ${i} "chmod +x *.sh ; ~/set1.sh  ; ./set2.sh ; ./update_grub.sh ; sudo reboot"
	ssh ${i} "chmod +x *.sh ; ~/set1.sh  ; ./update_grub.sh ; sudo reboot"
done

