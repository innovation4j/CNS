#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 2-1. 라즈베리 전체 전원 off
echo "2-1. [start] power off all raspberry pi"
# A 이면 라즈베리 전체 전원 Off
if [ x$app == x$a ]; then
    curl http://127.0.0.1:5000/rasoff
else
    echo="no flask running server !!!"
    echo="no flask running server !!!"
    echo="no flask running server !!!"
fi
echo "2-1. [done] power off all raspberry pi"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!