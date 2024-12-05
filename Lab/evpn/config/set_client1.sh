for i in {1..3}
do 
    sudo ip netns add pe${i}
    sudo ip link set dev eth${i} netns pe${i}
    sudo ip netns exec pe${i} ip link set dev lo up
    sudo ip netns exec pe${i} ip addr add dev eth${i} 10.1.10${i}.10/24
    sudo ip netns exec pe${i} ip link set dev eth${i} up
    sudo ip netns exec pe${i} ip route add default via 10.1.10${i}.1
done

alias pe1="sudo ip netns exec pe1"
alias pe2="sudo ip netns exec pe2"
alias pe3="sudo ip netns exec pe3"

