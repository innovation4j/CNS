#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 5. 라즈베리 전체 전원 On
echo -e "\n5. [start] power on all raspberry pi"
# Flask 구동서버가 맞으면 라즈베리 전체 전원 On 실행
if [ x$app == x$a ]; then
    echo "yes flask running server !!!"
    while :
    do
    status_code=$(curl --write-out %{http_code} --silent --output ./ -L http://127.0.0.1:5000/)
        if [[ "$status_code" -ne 200 ]] ; then
            sleep 1s
            echo "Wait 1 second for Flask to turn on"
        else
            echo -e "Flask is on now!"
            echo -e "run RPI Power On"
            curl http://127.0.0.1:5000/rason
            echo -e "\n"
            break
        fi
        # 지연시간 추가
        sleep 0.1s
    done
    source /home/iot/Documents/CNS/cns_script_rpi_check.sh
else
    echo "no flask running server !!!"
    echo "no flask running server !!!"
fi
sleep 3s
echo -e "5. [done] power on all raspberry pi \n"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

