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
        self.seq_number = data[10]
        self.pkt_id = data[11]


with open('../trace_files/trace_files_tcp_tahoe/exp1_tahoe_6.tr') as f:
    content = f.readlines()

first_line = content[0].split()
last_line = content[-2].split()

start_time = float(first_line[1])
end_time = float(last_line[1])

packets_dropped = 0
enqueue = 0

for c in content:
    packet = Packet(c.split())
    if packet.event == 'd' and packet.flow_id == '2':
        packets_dropped += 1
    if packet.event == '+' and packet.flow_id == '2':
        enqueue += 1

print "Packets dropped:::", packets_dropped
print "Packet drop rate:::", float(packets_dropped) / enqueue
# print float(packets_dropped) / len(content)