#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 2-2. 라즈베리 전체 전원 On
echo "2-1. [start] power on all raspberry pi"
# A 이면 라즈베리 전체 전원 On
if [ x$app == x$a ]; then
    echo "yes flask running server !!!"
    curl http://127.0.0.1:5000/rason
else
    echo "no flask running server !!!"
    echo "no flask running server !!!"
fi
echo "2-1. [done] power on all raspberry pi"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

source /home/iot/Documents/CNS/cns_script_rpi_check.sh