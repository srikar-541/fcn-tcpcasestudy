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


with open('../trace_files/newreno_reno/exp2_2_10.tr') as f:
    content = f.readlines()

pkts_rcvd1 = 0
pkts_rcvd2 = 0
start_time_1 = -1
start_time_2 = -1
end_time_1 = 0
end_time_2 = 0
dict1 = {}
dict2 = {}
total_delay1 = 0.0
total_delay2 = 0.0

for line in content:
    packet = Packet(line.split())
    if packet.pkt_type == "tcp" and packet.event == "+" and float(packet.from_node) == float(packet.source_addr):
        if packet.flow_id == "2":
            dict1[packet.seq_number] = packet.time
            if start_time_1 == -1:
                start_time_1 = packet.time
        else:
            dict2[packet.seq_number] = packet.time
            if start_time_2 == -1:
                start_time_2 = packet.time
    elif packet.pkt_type == "ack" and packet.event == "r" and float(packet.to_node) == float(packet.dest_addr):
        if packet.flow_id == "2" and packet.seq_number in dict1:
            pkts_rcvd1 += 1
            total_delay1 += packet.time - dict1[packet.seq_number]
            end_time_1 = packet.time
        elif packet.flow_id == "3" and packet.seq_number in dict2:
            pkts_rcvd2 += 1
            total_delay2 += packet.time - dict2[packet.seq_number]
            end_time_2 = packet.time

delay1 = 0 if pkts_rcvd1 == 0 else total_delay1 / pkts_rcvd1
delay2 = 0 if pkts_rcvd2 == 0 else total_delay2 / pkts_rcvd2

print "End to End Delay1:::", delay1
print "End to End Delay2:::", delay2
