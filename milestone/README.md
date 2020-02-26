For each experiment, we will examine and analyse trace file data such as average bandwidth, packet drops, throughput over time, end-to-end latency (average and over time), sequence numbers of packets sent, and the congestion window of all TCP flows.

Because TCP performs poorly when there is a high bandwidth-delay product, we plan to run all experiments by changing the delay and bandwidth settings between each node to see how the different variants of TCP behave.
TCP performance also depends on the timing of flow start times between the comparisons.

Experiment 1:TCP performance under congestion.

For each of the TCP variants (Tahoe, Reno, NewReno, and Vegas), we plan to start the CBR flow at a rate of 1 Mbps and record the performance of the TCP flow. For the consecutive experiments we will increase the CBR flow rate by 0.5Mbps until it reaches the bottleneck capacity. For each TCP variant, we run this experiment 100 times.

When CBR is increased, because the sole purpose of CBR is to increase the traffic and it doesn’t expect any acknowledgments for the data it sends out and doesn’t follow any principles like exponential backoff or waiting for a certain amount of time before retrying unlike tcp packets, there will be a significant drop in the number of packets dropped. With increase in CBR, number of packets sent through the TCP flow also reduces naturally, thereby reducing the overall throughput. For the same reason, the latency of the TCP stream will also reduce as the CBR increases.
TCP performance also depends on the timing of flow start times between the comparisons.
For this purpose, we plan to send CBR first for a certain amount of time, then include the TCP flow for some time. We can also run this under different settings like sending TCP flow first and CBR later.

We also plan to experiment with a variety of CBR flow packet size and interval to see how this impacts the TCP flow.

Experiment 2

For each pair of TCP variants
Reno/Reno
NewReno/Reno
Vegas/Vegas
NewReno/Veg
We follow the exact same steps as in Experiment 1. As an additional step, since we have two flows N1 N4 and N5 N6, we run a combination of TCP variants in them. For example, for NewReno/Reno, we choose the N1 N4 flow to be NewReno and N5 N6 flow to be Reno. 
Fairness also depends on which TCP protocol was first used to send the flow. One TCP flow can use up all the resources, leaving the other flow with little bandwidth. To understand the effect of this, we plan to run this by changing which flow to use first.
We can comment about the fairness of a pair of variants only after running the different combinations.

Experiment 3

We plan to first run the TCP flow for some time till the network stabilizes,after which we introduce a CBR flow at a fixed rate and examine how they behave under Droptail and RED queuing algorithms.  
We plan to experiment with a couple of queue sizes. We get 4 combinations of TCP variants and queuing algorithms(Reno RED, SACK RED, Reno DropTail, SACK DropTail).
The best combination of the TCP variant and the queuing algorithm will be decided based on the average bandwidth and latency parameters.

