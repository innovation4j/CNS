#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 1. cns_detection.py 프로세스를 전부 종료
echo -e "\n$today $hms 1. [start] kill cns_detection.py"
pkill -9 -ef cns_detection.py
echo "$today $hms pkill -9 -ef cns_detection.py"
echo -e "$today $hms 1. [done] kill cns_detection.py \n"
sleep 3s
ps -aux | grep cns
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!