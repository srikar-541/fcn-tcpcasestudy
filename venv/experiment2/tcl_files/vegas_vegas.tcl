set ns [new Simulator]


set tf [open exp2_1.tr w]
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
$cbr set rate_ 2Mb
$cbr set random_ false

# FIRST TCP FLOW
# Setting up a TCP flow
set tcp1 [new Agent/TCP/Vegas]
# $tcp set class_ 2
$ns attach-agent $n1 $tcp1

set sink1 [new Agent/TCPSink]
$ns attach-agent $n4 $sink1
$ns connect $tcp1 $sink1
$tcp1 set fid_ 2


# Setup FTP over TCP
# experiment with different Application protocols.
# mix of application protocols?
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP


# SECOND TCP FLOW
# Setting up a TCP flow
set tcp2 [new Agent/TCP/Vegas]
# $tcp set class_ 2
$ns attach-agent $n5 $tcp2

set sink2 [new Agent/TCPSink]
$ns attach-agent $n6 $sink2
$ns connect $tcp2 $sink2
$tcp2 set fid_ 3


# Setup FTP over TCP
# experiment with different Application protocols.
# mix of application protocols?
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set type_ FTP

proc finish {} {
	global ns tf
	$ns flush-trace
	close $tf
	exit 0
}

#Schedule events for the CBR and FTP agents
$ns at 0.1 "$cbr start"
$ns at 1.0 "$ftp1 start"
$ns at 2.0 "$ftp2 start"
$ns at 5.0 "$ftp2 stop"
$ns at 5.9 "$ftp1 stop"
$ns at 6.5 "$cbr stop"
$ns at 7 "finish"


# Close the trace file (after you finish the experiment!)
$ns run

