#!/bin/bash

server="192.168.1.240"
port=1883
topic="ca_ses_llucies/1/system_state"
states=('HOME' 'TRACKING' 'GHOST')

while [ 1 ]
do
	uwait=$(($RANDOM % 3))
	message=${states[$uwait]}
	echo "Sending to $server:$port on topic '$topic' message '$message'";
	mosquitto_pub -h $server -p $port -t "$topic" -m "$message";
	sleep $uwait
done
