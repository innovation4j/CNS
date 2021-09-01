#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 1. cns_detection.py 프로세스를 전부 종료
echo -e "\n$today $hms [start] detection_stop.sh"

for var in {1..7} ; do
    echo "$today $hms XXXXXX | sudo -S systemctl stop cns_detection_$lineip$var"
    echo $SUDOPW | sudo -S systemctl stop cns_detection_$lineip$var
done

pkill -9 -ef cns_detection.py
echo "$today $hms pkill -9 -ef cns_detection.py"

echo -e "$today $hms [done] detection_stop.sh \n"
sleep 3s
ps -aux | grep cns
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!