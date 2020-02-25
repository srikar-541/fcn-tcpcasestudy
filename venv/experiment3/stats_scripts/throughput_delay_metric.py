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


with open('../trace_files/exp3_DROP_RENO.tr') as f:
    content = f.readlines()

print len(content)
pkts_rcvd = 0
start_time = 0
map = {}
delay = 0
values = [()]
throughput = 0

for line in content:
    packet = Packet(line.split())
    # print packet
    if packet.pkt_type == "tcp" and packet.event == "+":
        map[packet.seq_number] = packet.time

    if packet.pkt_type == "ack" and packet.event == "r":
        if packet.seq_number in map:
            pkts_rcvd += 1
            delay += packet.time - map.pop(packet.seq_number)

    if packet.time - start_time >= 1:
        throughput = pkts_rcvd * 8 * 1040 / (packet.time - start_time) / 1048576
        delay = delay / pkts_rcvd
        values.append((packet.time, throughput, delay))
        start_time = packet.time
        map = {}
        pkts_rcvd = 0
        delay = 0

values.append((10, throughput, delay))
for v in values:
    print v
