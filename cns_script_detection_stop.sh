#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 1. cns_detection.py 프로세스를 전부 종료
echo "1. [start] kill cns_detection.py"
pkill -9 -ef cns_detection.py
echo"pkill -9 -ef cns_detection.py"
echo "1. [done] kill cns_detection.py"
ps -aux | grep cns
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!