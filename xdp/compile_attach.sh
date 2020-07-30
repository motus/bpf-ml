#enter interface names as cmd line input
if [ $# -ne 1 ];then
	echo "Usage: ./compile_attach.sh <interface> "
	exit 0
fi

clang-9 -Wno-unused-value -Wno-pointer-sign -Wno-compare-distinct-pointer-types -Wno-gnu-variable-sized-type-not-at-end -Wno-tautological-compare -g -c -O2 -S -emit-llvm xdp.c -o -| llc-9 -march=bpf -filetype=obj -o xdp.o

sudo ip link set dev $1 xdp obj xdp.o