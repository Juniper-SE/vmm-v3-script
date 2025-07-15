for i in director os cc cadb can compute{1..3}
do
scp ~/.ssh/keylab ${i}:~/
scp ~/.ssh/keylab.pub ${i}:~/
ssh ${i} "sudo mkdir /home/stack/.ssh; sudo cp /home/rhel/keylab /home/stack/.ssh/id_rsa;sudo cp /home/rhel/keylab.pub /home/stack/.ssh/authorized_keys ; sudo chown -R stack:stack /home/stack/.ssh; sudo chmod -R og-rwx /home/stack/.ssh"
done

scp ~/.ssh/keylab gw:~/.ssh/
scp ~/.ssh/keylab.pub gw:~/.ssh/
