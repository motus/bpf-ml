# Bringing Machine Learning to the OS Kernel

This is a
[Hackathon 2020 project](https://garagehackbox.azurewebsites.net/hackathons/2107/projects/95518)
that explores (and confirms) the possibility of evaluating machine learning models inside the Linux
kernel. In this hack, we use PyTorch to train a binary classifier to distinguish between malicious
and benign IP traffic and translate this model into
[eBPF](https://en.wikipedia.org/wiki/Berkeley_Packet_Filter)-based
[XDP](https://en.wikipedia.org/wiki/Express_Data_Path) packet filter.

# Documents

* [Our vision document](https://1drv.ms/w/s!AqyekuzAVCpuhSNyXus1kYn6e3Fw?e=IXfUDa)
* [Our Hackathon 2020 presentation slides](https://microsoft-my.sharepoint-df.com/:p:/p/sergiym/EcPPhtfKR8RChBEBwDJfzmABhUKoXr9nQE0AT2XIF8l7Zw?e=796rWe)
* [Hackathon 2020 page and **screencast**](https://garagehackbox.azurewebsites.net/hackathons/2107/projects/95518)

# Our vision

There is a growing need to make complex data-driven decisions early in the OS event processing
pipeline. The examples can be filtering of the IP traffic, early detection of suspicious network
activity, or real-time analysis of the software behavior for better application security, debugging,
and resource allocation. *We want to develop a technology for secure evaluation of arbitrary machine
learning models in the OS kernel.*

## State of the art

As of now, the use of machine learning at the kernel level is virtually non-existent. At best,
engineers use kernel-level features to collect the data and evaluate ML models in userland or use ML
to create IP filtering rules. Surprisingly, Linux and *BSD already have the technology that can
securely run ML models in the kernel. It is eBPF, or (extended) Berkeley Packet Filter. It was
designed as a runtime for executing user-defined packet filtering rules early in the network stack.
However, its in-kernel bytecode engine (along with a JIT compiler) is not limited to network
applications. In the last three years, it became extremely popular in the Linux community, and the
ecosystem of eBPF-based tools for performance analysis, forensics, and debugging has emerged.

We believe that eBPF can be a great vehicle for bringing ML models closer to the kernel. There is
very little prior art in this area. To our best knowledge, there are only two research publications
on using ML models in eBPF, and, in both cases, researchers had translated the existing simple ML
models from a high-level language into eBPF bytecode by hand.

## What's new

*We will build a compiler that takes an arbitrary ML model in some widely used format (e.g., ONNX or
TensorFlow) and converts it into eBPF bytecode.* Our system will allow ML practitioners to train
models in their popular ML framework, like PyTorch or Keras, and securely deploy them in Linux or
*BSD kernel. This way, we can bring complex deep learning models to the kernel and make their
release cycle very short.

## Payoffs

On success, Microsoft will establish itself as a leader in kernel-level machine learning and improve
its reputation in Linux and BSD communities. We can use kernel-level machine learning internally on,
e.g., Cosmos or Bing, to enhance the security and reliability of our services. Better yet, we can
extend AzureML service to deploy models straight to the kernel of user VMs on Azure, and even
provide pre-trained models as a service to the Azure users. That can give Azure a significant
competitive advantage over Amazon and Google cloud services.
