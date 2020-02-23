set ns [new Simulator]


set tf [open exp1_4_10.tr w]
$ns trace-all $tf



set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]


# experiment with delay and queueing algorithm
$ns duplex-link $n2 $n3 10Mb 2ms DropTail
$ns duplex-link $n1 $n2 10Mb 2ms DropTail
$ns duplex-link $n5 $n2 10Mb 2ms DropTail
$ns duplex-link $n3 $n4 10Mb 2ms DropTail
$ns duplex-link $n3 $n6 10Mb 2ms DropTail

# setting queue size for n2-n3 experiment
# $ns queue-limit $n2 $n3 10

#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp

set null [new Agent/Null]
$ns attach-agent $n3 $null

$ns connect $udp $null
$udp set fid_ 1


#Setup a CBR over UDP connection
# experiment  with values.
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ 10Mb
$cbr set random_ false



# Setting up a TCP flow
set tcp [new Agent/TCP/Reno]
# $tcp set class_ 2
$ns attach-agent $n1 $tcp

set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set fid_ 2


# Setup FTP over TCP
# experiment with different Application protocols.
# mix of application protocols?
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP


proc finish {} {
	global ns tf
	$ns flush-trace
	close $tf
	exit 0
}

#Schedule events for the CBR and FTP agents
$ns at 0.1 "$cbr start"
$ns at 1.0 "$ftp start"
$ns at 4.0 "$ftp stop"
$ns at 4.5 "$cbr stop"
$ns at 5 "finish"


# Close the trace file (after you finish the experiment!)
$ns run

