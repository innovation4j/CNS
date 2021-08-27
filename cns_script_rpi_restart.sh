#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 2. 라즈베리를 전체 리스타트
echo "2. [start] restart raspberry pi"
# A 이면 라즈베리를 전체 리스타트 실행
if [ x$app == x$a ]; then
    echo "yes flask running server !!!"
    curl http://127.0.0.1:5000/reset
else
    echo="no flask running server !!!"
    echo="no flask running server !!!"
fi
echo "2. [done] restart raspberry pi"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 3. 리셋 완료까지 2분 가량 sleep
echo "3. [start] sleep 120s"
sleep 1s
echo "sleep 1s"
echo "3. [done] sleep 120s"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

source /home/iot/Documents/CNS/cns_script_rpi_check.sh