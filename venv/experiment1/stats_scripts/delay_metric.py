class Packet:
    def __init__(self, data):
        self.event = data[0]
        self.time = float(data[1])
        self.from_node = data[2]
        self.to_node = data[3]
        self.pkt_type = data[4]
        self.pkt_size = int(data[5])
        self.flow_id = data[7]
        self.source_addr = data[8]
        self.dest_addr = data[9]
        self.seq_number = int(data[10])
        self.pkt_id = data[11]


packets = []
with open('../trace_files/trace_files_reno/exp1_4_10.tr') as f:
    content = f.readlines()

for line in content:
    line = line.split()
    if len(line) < 10:
        continue
    packet = Packet(line)
    packets.append(packet)

packets = filter(lambda x: x.pkt_type != 'cbr', packets)
# print len(packets)
total_latency = 0.0

# for packet in packets:
#     print packet.__dict__
#
# for packet in packets:
#     print packet.__dict__
pkts_rcvd = 0
total_latency = 0
for i in range(1, len(packets)):
    current_packet = packets[i - 1]

    if current_packet.event == 'r':
        end_time = current_packet.time

        j = i - 1
        while j > 0:
            prev_packet = packets[j]
            if prev_packet.event == '+' and current_packet.seq_number == prev_packet.seq_number:
                start_time = prev_packet.time
                # print current_packet.__dict__, prev_packet.__dict__
                total_latency += end_time - start_time
                pkts_rcvd += 1
                break
            j = j - 1
print "End to end delay::::", total_latency
print "Average End to End delay::::", total_latency / pkts_rcvd
print "Packets received::::", pkts_rcvd
