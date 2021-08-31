#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 5. 라즈베리를 전체 리스타트
echo -e "\n$today $hms 5-3. [start] restart raspberry pi"
# Flask 구동서버가 맞으면 라즈베리를 전체 reset 실행
if [ x$app == x$a ]; then
    echo "$today $hms yes flask running server !!!"
    while :
    do
    status_code=$(curl --write-out %{http_code} --silent --output ./ -L http://127.0.0.1:5000/)
        if [[ "$status_code" -ne 200 ]] ; then
            sleep 1s
            echo "$today $hms Wait 1 second for Flask to turn on"
        else
            echo -e "$today $hms Flask is on now!"
            echo -e "$today $hms run RPI Power reset"
            curl http://127.0.0.1:5000/reset
            echo -e "$today $hms \n"
            break
        fi
        # 지연시간 추가
        sleep 0.1s
    done
    source $shomedir/rpi_check.sh
else
    echo "$today $hms no flask running server !!!"
    echo "$today $hms wait 30 seconds !!!"
    SET=$(seq 1 30)
    for i in $SET
    do
        sleep 1s
        echo "$today $hms $i s"
    done
    source $shomedir/rpi_check.sh
fi
sleep 3s
echo -e "$today $hms 5-3. [done] power on all raspberry pi \n"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!