
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
    -28,  -86,  -48,   90, -113,   34,  127,   83, -107,    3,  -70,  -63,
     10,  -17,  -27,   26,   -3,  -70,  -58,  127,    5,   60,  -36,  -46,
    -11,  102,   14,   18,  -99,   88,  101,  -29,   86,    4
};

static int b = 5;

SEC("prog")
int xdp(struct xdp_md *ctx)
{
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;

    u16 h_proto;
    u64 nh_off = 0;
    u32 index;

    struct ethhdr *eth;
    struct iphdr *iph;

    s64 y = b;                                         // start with the bias; no need to clamp y
    h_proto = parse_eth(data, nh_off, data_end, eth);  // get the eth header
    nh_off = sizeof(*eth);

    if (h_proto == htons(ETH_P_IP))
    {
        index = parse_ipv4(data, nh_off, data_end, iph); //get the ipv4 header
        nh_off = sizeof(*iph);
        if (data_end < data + (34))
        { //verification
            return XDP_PASS;
        }

        // y=w*x+b start
        #pragma unroll
        for (u8 i = 0; i < 34; ++i)
        {
            s8 *byte = data + (i); // don't change this
            s64 prod = (*byte) * w[i];
            if (prod < -128)
                prod = -128;
            else if (prod > 127)
                prod = 127;
            y += prod;
        }
        // y=w*x+b stop

        if (y > 0)
        {
            printk("Dropping: %d\n", y);
            return XDP_DROP; // droping spam packets
        }
    }

    printk("Passing: %d\n", y);
    return XDP_PASS; // passing correct packets
}

char _license[] SEC("license") = "GPL";
