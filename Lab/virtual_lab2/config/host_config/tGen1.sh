#!/bin/bash
## configuration on tGEN

cat << EOF | tee -a ~/.profile
alias vrf1_eth1="sudo  ip netns exec vrf1_eth1"
alias vrf2_eth2="sudo  ip netns exec vrf2_eth2"
alias vrf3_eth3="sudo  ip netns exec vrf3_eth3"
alias vrf4_eth4="sudo  ip netns exec vrf4_eth4"
alias cust1_eth1="sudo  ip netns exec cust1_eth1"
alias cust1_eth2="sudo  ip netns exec cust1_eth2"
alias cust1_eth3="sudo  ip netns exec cust1_eth3"
alias cust1_eth4="sudo  ip netns exec cust1_eth4"
EOF

