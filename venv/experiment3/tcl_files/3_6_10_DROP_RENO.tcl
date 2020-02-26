set ns [new Simulator]

set tf [open exp3_6_7_DROP_RENO.tr w]
$ns trace-all $tf


#Create six nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n5 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail

#set queue size
$ns queue-limit	$n1 $n2 10
$ns queue-limit	$n5 $n2 10
$ns queue-limit	$n2 $n3 10
$ns queue-limit	$n4 $n3 10
$ns queue-limit	$n6 $n3 10

#Set CBR agent.
set udp [new Agent/UDP]
$ns attach-agent $n5 $udp
set cbr [new Application/Traffic/CBR]
$cbr set rate_ 8Mb
$cbr attach-agent $udp
set null [new Agent/Null]
$ns attach-agent $n6 $null

set tcp [new Agent/TCP/Reno]
$ns attach-agent $n1 $tcp

set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink

set ftp [new Application/FTP]
$ftp attach-agent $tcp

$ns connect $udp $null
$udp set fid_ 1
$ns connect $tcp $sink
$tcp set fid_ 2

$ns at 0.0 "$ftp start"
$ns at 6.0 "$cbr start"
$ns at 20.0 "$ftp stop"
$ns at 20.0 "$cbr stop"
$ns at 20.5 "finish"

$ns run

