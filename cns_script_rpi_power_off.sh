#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 2. 라즈베리 전체 전원 off
echo -e "\n2. [start] power off all raspberry pi"
# Flask 구동서버가 맞으면 라즈베리 전체 전원 Off 실행
if [ x$app == x$a ]; then
    echo "yes flask running server !!!"
    curl http://127.0.0.1:5000/rasoff
else
    echo "no flask running server !!!"
    echo "wait 10 seconds !!!"
    SET=$(seq 0 9)
    for i in $SET
    do
        sleep 1s
        echo "$i s"
    done
fi
sleep 3s
echo -e "2. [done] power off all raspberry pi \n"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!