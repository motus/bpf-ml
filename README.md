# Bringing Machine Learning to the OS Kernel

This is a [Hackathon 2020 project](https://garagehackbox.azurewebsites.net/hackathons/2107/projects/95518) that explores (and confirms) the possibility of evaluating machine learning models inside the Linux kernel.
In this hack, we use PyTorch to train a binary classifier to distinguish between malicious and benign IP traffic and translate this model into [eBPF](https://en.wikipedia.org/wiki/Berkeley_Packet_Filter)-based [XDP](https://en.wikipedia.org/wiki/Express_Data_Path) packet filter.

To reproduce the results:

1. Collect some positive and negative data samples in [PCAP](https://www.tcpdump.org/manpages/pcap.3pcap.html) format (e.g., using [tcpdump](https://www.tcpdump.org)).
   This repo has some sample packets in [`data/`](data) directory.
2. Train your classifier (run [`model/model.py`](model/model.py) script).
3. Copy the quantized weight of your model into array `w` in [`xdp/xdp.c`](xdp/xdp.c).
   (Yeah, we should've generated a source file instead)..
4. Compile your C code and install the eBPF module by running [`xdp/compile_attach.sh`](xdp/compile_attach.sh) script.
5. To uninstall the packet filter, run [`xdp/remove.sh`](xdp/remove.sh).

> Please note that this project is merely a proof-of-concept hack and is not supported by the developers.
> Feel free to fork and move it forward, and we'll send you our kudos and PRs!
