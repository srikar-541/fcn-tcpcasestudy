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


with open('../trace_files/reno_reno/exp2_1_10.tr') as f:
    content = f.readlines()

pkts_rcvd1 = 0
pkts_rcvd2 = 0
start_time_1 = -1
start_time_2 = -1
end_time_1 = 0
end_time_2 = 0
set1 = set()
set2 = set()

for line in content:
    packet = Packet(line.split())
    if packet.pkt_type == "tcp" and packet.event == "+":
        if packet.flow_id == "2":
            set1.add(packet.seq_number)
            if start_time_1 == -1:
                start_time_1 = packet.time
        else:
            set2.add(packet.seq_number)
            if start_time_2 == -1:
                start_time_2 = packet.time

    if packet.pkt_type == "ack" and packet.event == "r":
        if packet.flow_id == "2" and set1.__contains__(packet.seq_number):
            pkts_rcvd1 += 1
            end_time_1 = packet.time
            set1.remove(packet.seq_number)
        elif packet.flow_id == "3" and set2.__contains__(packet.seq_number):
            pkts_rcvd2 += 1
            end_time_2 = packet.time
            set2.remove(packet.seq_number)

tp1 = (pkts_rcvd1 * 1040 * 8) / (end_time_1 - start_time_1) / 1048576
tp2 = (pkts_rcvd2 * 1040 * 8) / (end_time_2 - start_time_2) / 1048576

print "Throughput:::", tp1
print "Throughput:::", tp2

