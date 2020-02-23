set ns [new Simulator]


set tf [open exp3_1_1.tr w]
$ns trace-all $tf


set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]


# experiment with delay and queueing algorithm

$ns duplex-link $n2 $n3 10Mb 2ms RED
$ns duplex-link $n1 $n2 10Mb 2ms RED
$ns duplex-link $n5 $n2 10Mb 2ms RED
$ns duplex-link $n3 $n4 10Mb 2ms RED
$ns duplex-link $n3 $n6 10Mb 2ms RED

#set queue size
$ns queue-limit	$n1 $n2 10
$ns queue-limit	$n5 $n2 10
$ns queue-limit	$n2 $n3 10
$ns queue-limit	$n4 $n3 10
$ns queue-limit	$n6 $n3 10

#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n5 $udp
set null [new Agent/Null]
$ns attach-agent $n6 $null
$ns connect $udp $null
$udp set fid_ 2


#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ 6Mb
$cbr set random_ true


#Setup a TCP connection
set tcp [new Agent/TCP/Sack1]
$ns attach-agent $n1 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set fid_ 1
$tcp attach-trace $tcpfile
$tcp trace cwnd_

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP

# Setup FTP over TCP
# experiment with different Application protocols.
# mix of application protocols?
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP


proc finish {} {
	global ns tf
	$ns flush-trace
	close $tf
	exit 0
}

#Schedule events for the CBR and FTP agents
$ns at 0.0 "$ftp start"
$ns at 5.0 "$cbr start"
$ns at 9.0 "$ftp stop"
$ns at 9.5 "$cbr stop"

$ns at 10 "finish"

$ns run

close $tf

