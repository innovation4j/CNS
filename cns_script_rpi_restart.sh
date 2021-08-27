#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 5. 라즈베리를 전체 리스타트
echo -e "\n5. [start] restart raspberry pi"
# Flask 구동서버가 맞으면 라즈베리를 전체 reset 실행
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
            echo -e "run RPI Power reset"
            curl http://127.0.0.1:5000/reset
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