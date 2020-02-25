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


with open('../trace_files/exp3_RED_SACK.tr') as f:
    content = f.readlines()

packets_dropped = 0
enqueue = 0
set = set()

for c in content:
    line = c.split()
    packet = Packet(line)
    if packet.event == '+':
        if packet.flow_id == '1' and not set.__contains__(packet.pkt_id):
            enqueue += 1
            set.add(packet.pkt_id)
    if packet.event == 'd':
        if packet.flow_id == '1' and set.__contains__(packet.pkt_id):
            packets_dropped += 1
            set.remove(packet.pkt_id)

print "Packet drop rate:::", float(packets_dropped) / enqueue