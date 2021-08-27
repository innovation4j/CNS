#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 5. App.py 프로세스 종료
echo "5. [start] App.py 프로세스 종료"
if [ x$app == x$a ]; then
    echo "yes flask running server !!!"
    #sudo ps -ef | grep app.py | awk '{print $2}' | xargs kill -9
    echo $SUDOPW | sudo -S systemctl stop plotter_runner
    sleep 3s
else
    echo "no flask running server !!!"
    echo "no flask running server !!!"
fi
echo "5. [done] App.py 프로세스 종료"
ps -aux | grep app.py
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!