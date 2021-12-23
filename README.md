# Bringing Machine Learning to the OS Kernel

This is a
[Hackathon 2020 project](https://garagehackbox.azurewebsites.net/hackathons/2107/projects/95518)
that explores (and confirms) the possibility of evaluating machine learning models inside the Linux
kernel. In this hack, we use PyTorch to train a binary classifier to distinguish between malicious
and benign IP traffic and translate this model into
[eBPF](https://en.wikipedia.org/wiki/Berkeley_Packet_Filter)-based
[XDP](https://en.wikipedia.org/wiki/Express_Data_Path) packet filter.

