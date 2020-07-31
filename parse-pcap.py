#!/usr/bin/env python3

import pickle
from scapy.utils import RawPcapReader


def parse(fname):
    return [[b for b in pkt] for (pkt, _meta) in RawPcapReader(fname)]


for fname in ["nmap", "scp"]:
    data = parse("data/%s.pcap" % fname)
    print("%s data has %d packets" % (fname, len(data)))
    with open("data/%s.pk" % fname, "wb") as pkfile:
        pickle.dump(data, pkfile)
