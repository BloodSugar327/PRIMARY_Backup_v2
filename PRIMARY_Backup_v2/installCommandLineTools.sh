#!/bin/bash


pids=""
RESULT=0


for i in `seq 0 9`; do
   xcode-select --install
   pids="$pids $!"
done

for pid in $pids; do
	wait $pid || let "RESULT=1"
done

if [ "$RESULT" == "1" ];
	then
	   exit 1
fi