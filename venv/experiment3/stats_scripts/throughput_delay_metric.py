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


with open('../trace_files/exp3_6_7_RED_SACK.tr') as f:
    content = f.readlines()

print len(content)
pkts_rcvd = 0
start_time = 0
map = {}
delay = 0
values = [()]
throughput = 0
enqueue = 0
packets_dropped = 0
set = set()
k = 0
try:
    for line in content:
        k = line.split()
        if len(line) < 11:
            continue
        packet = Packet(k)
        # print packet.__dict__
        if packet.pkt_type == "tcp" and packet.event == "+":
            map[packet.seq_number] = packet.time

        if packet.pkt_type == "ack" and packet.event == "r":
            if packet.seq_number in map:
                pkts_rcvd += 1
                delay += packet.time - map.pop(packet.seq_number)

        if packet.event == '+':
            if packet.flow_id == '2' and not set.__contains__(packet.pkt_id):
                enqueue += 1
                set.add(packet.pkt_id)
        if packet.event == 'd':
            if packet.flow_id == '2' and set.__contains__(packet.pkt_id):
                packets_dropped += 1
                set.remove(packet.pkt_id)

        if packet.time - start_time >= 1:
            throughput = pkts_rcvd * 8 * 1040 / (packet.time - start_time) / 1048576
            delay = delay / pkts_rcvd
            values.append((packet.time, throughput, delay, float(packets_dropped) / enqueue))
            start_time = packet.time
            map = {}
            set.clear()
            packets_dropped = 0
            enqueue = 0
            pkts_rcvd = 0
            delay = 0
except:
    print k


#values.append((20, pkts_rcvd * 8 * 1040 / (20 - start_time) / 1048576, delay / pkts_rcvd, float(packets_dropped) / enqueue))
for v in values:
    print v
