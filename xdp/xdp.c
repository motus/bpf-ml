#include "headers/linux/bpf.h"
#include "headers/bpf_helpers.h"
#include <stdio.h> 
#include <stdbool.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/if_vlan.h>
#include <linux/ip.h>
#include <linux/ipv6.h>
#include "xdp.h"
static int w[34] = {
        -3334974,
        -641339,
        -32066,
        -3399095,
        -5964459,
        -6445474,
        -1539213,
        -7920535,
        -3655627,
        -2212619,
        -5804102,
        -7471618,
        -256536,
        0,
        -2212620,
        -5928,
        -9,
        -1548928,
        -2338445,
        -3688329,
        -1391441,
        -0,
        -1887207,
        -192360,
        -6027544,
        -4035183,
        -6156854,
        -5387251,
        -929945,
        -6862365,
        -4371700,
        -3960792,
        -4829687,
        -5764115
    };
static int b = -32066;
SEC("prog")
int xdp(struct xdp_md *ctx) {
    
    void* data_end = (void*)(long)ctx->data_end;
    void* data = (void*)(long)ctx->data;
     u16 h_proto;
    u64 nh_off = 0;
    u32 index;
    struct ethhdr *eth;
    struct iphdr *iph;
    s8 y=0;           
    h_proto = parse_eth(data,nh_off,data_end,eth); //get the eth header
    nh_off = sizeof(*eth);
    if (h_proto == htons(ETH_P_IP)){
       index = parse_ipv4(data, nh_off, data_end,iph); //get the ipv4 header
       nh_off = sizeof(*iph);
        if(data_end<data+(34)){ //verification
            return XDP_PASS;
        }
     //y=w*x+b start
       #pragma unroll 
        for(int i=0;i<34;i++){
            s8 *byte = data+(i);
            u8 *d = data+(i);
            y+=*byte+(s8)w[i];
        }
        y += (s8)b;
        //y=w*x+b stop
        if(y>0){
            printk("Dropping: %d\n",y);
            return XDP_DROP; //droping spam packets
        }
       
    }
    printk("Passing: %d\n",y);
    return XDP_PASS; // passing correct packets

}
char _license[] SEC("license") = "GPL";