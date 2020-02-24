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


with open('../trace_files/trace_files_reno/exp1_Reno_10.tr') as f:
    content = f.readlines()

packets_sent = 0
packets_received = 0
start_time = -1
end_time = 0
set1 = set()

for line in content:
    line = line.split()
    if len(line) < 10:
        continue
    packet = Packet(line)

    if packet.event == '+' and packet.pkt_type == "tcp":
        if start_time == -1:
            start_time = packet.time
        set1.add(packet.seq_number)
    if packet.event == 'r' and packet.pkt_type == 'ack' and set1.__contains__(packet.seq_number):
        packets_received += 1
        end_time = packet.time
        set1.remove(packet.seq_number)

print "Throughput:::", packets_received * 1040 * 8 / (end_time - start_time) / (1024 * 1024)
