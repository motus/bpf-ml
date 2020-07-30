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

// #define SRC_IP 0xc0a81d10

// 192.168.1.118
#define SRC_IP 0xC0A80176

struct bpf_map_def SEC("maps") counter_pass = {
    .type        = BPF_MAP_TYPE_ARRAY,
    .key_size    = sizeof(u32),
    .value_size  = sizeof(u32),
    .max_entries = 1,
};

struct bpf_map_def SEC("maps") counter_drop = {
    .type        = BPF_MAP_TYPE_ARRAY,
    .key_size    = sizeof(u32),
    .value_size  = sizeof(u32),
    .max_entries = 1,
};

static int w[40] = {
    -30,  -93, -128,   -2,    8,   18,  -30,   -2,    28,  -20,
     -5,   46,   46,   -5,  -90,  -14,   29,   23,   -20,  -24,
     58,  -52,  -36,  -18,  -65,  -26,   80,  -20,  -103,  -41,
      6,   20,    8,   13,   23,  -40,    7,   37,   -60,   25
};

static int b = -50;

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

    s64 y = b;                                   // start with the bias; no need to clamp y
    h_proto = parse_eth(data, nh_off, data_end); // get the eth header
    eth = data;
    nh_off = sizeof(*eth);

    if (h_proto != htons(ETH_P_IP))
    {
        return XDP_PASS;
    }

    index = parse_ipv4(data, nh_off, data_end); // get the ipv4 header
    if (index != 6)                             // check if TCP packet or not
    {
        return XDP_PASS;
    }

    iph = data + nh_off;
    nh_off = sizeof(*iph);

    if (data_end < data + (54)) // eth+ipv4+tcp=54
    {                           // verification
        return XDP_PASS;
    }

    // pass all packets from hosts that are not in demo
    if (!(iph && ntohl(iph->saddr) == SRC_IP))
    {
        return XDP_PASS;
    }

    // y=w*x+b start
    #pragma unroll
    for (u8 i = 14; i < 54; ++i) //14th byte to 54th byte
    {
        s8 *byte = data + (i); // don't change this
        y += (*byte) * w[i];
    }
    // y=w*x+b stop

    u32 key = 0;
    u32 *val;

    if (y > 0)
    {
        val = bpf_map_lookup_elem(&counter_drop, &key);
        if (val)
        {
            (*val)++;
            printk("Dropping IP: %x Count: %d\n", ntohl(iph->saddr), *val);
        }
        return XDP_DROP; // droping spam packets
    }

    val = bpf_map_lookup_elem(&counter_pass, &key);
    if (val)
    {
        (*val)++;
        printk("Passing IP: %x Count: %d\n", ntohl(iph->saddr), *val);
    }

    return XDP_PASS; // passing correct packets
}

char _license[] SEC("license") = "GPL";
