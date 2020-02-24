class Packet:
    def __init__(self, data):
        self.event = data[0]
        self.time = data[1]
        self.from_node = data[2]
        self.to_node = data[3]
        self.pkt_type = data[4]
        self.pkt_size = int(data[5])
        self.flow_id = data[7]
        self.source_addr = data[8]
        self.dest_addr = data[9]
        self.seq_number = data[10]
        self.pkt_id = data[11]


with open('../trace_files/vegas_vegas/exp2_vegas_vegas_10.tr') as f:
    content = f.readlines()


packets_dropped1 = 0
packets_dropped2 = 0
enqueue1 = 0
enqueue2 = 0
set1 = set()
set2 = set()

for c in content:
    line = c.split()
    packet = Packet(line)
    if packet.event == '+':
        if packet.flow_id == '2' and not set1.__contains__(packet.pkt_id):
            enqueue1 += 1
            set1.add(packet.pkt_id)
        if packet.flow_id == '3' and not set2.__contains__(packet.pkt_id):
            set2.add(packet.pkt_id)
            enqueue2 += 1
    if packet.event == 'd':
        if packet.flow_id == '2':
            packets_dropped1 += 1
        if packet.flow_id == '3':
            packets_dropped2 += 1

print "Packets drop rate 1:::", float(packets_dropped1) / enqueue1
print "Packets drop rate 2:::", float(packets_dropped2) / enqueue2