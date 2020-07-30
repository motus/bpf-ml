
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

static int w[34] =
{
     94,   53,   63,   -8, -108,  -62,  -69,   99,   95,  -24,  -36,  -51,
     37,   28, -111,    5,  -16,  -76,  -22,   30, -128, -101,   34,   62,
    -27,   30,  -93,   76,   29,   89,   28,  117,   14,  -65
};

static int b = 17;

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
            y += (*byte) * w[i];
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
