#enter interface names as cmd line input
if [ $# -ne 1 ];then
	echo "Usage: ./compile_attach.sh <interface> "
	exit 0
fi

sudo ip link set dev $1 xdp off
if [ $? -eq 0 ]; then
    echo "XDP Prog removed from $1"
fi