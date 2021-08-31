#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 5. 라즈베리 전체 전원 On
echo -e "\n$today $hms [start] rpi_power_on.sh"
# Flask 구동서버가 맞으면 라즈베리 전체 전원 On 실행
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
            echo -e "$today $hms run RPI Power On"
            echo -e "\n$today $hms http://127.0.0.1:5000/rason"
            curl http://127.0.0.1:5000/rason
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
echo -e "$today $hms [done] rpi_power_on.sh \n"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

