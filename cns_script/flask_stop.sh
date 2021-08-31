#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 3. App.py 프로세스 종료
echo -e "\n$today $hms 3. [start] App.py 프로세스 종료"
if [ x$app == x$a ]; then
    echo "$today $hms yes flask running server !!!"
    #sudo ps -ef | grep app.py | awk '{print $2}' | xargs kill -9
    echo $SUDOPW | sudo -S systemctl stop plotter_runner
else
    echo "$today $hms no flask running server !!!"
    echo "$today $hms wait 10 seconds !!!"
    SET=$(seq 1 10)
    for i in $SET
    do
        sleep 1s
        echo "$today $hms $i s"
    done
fi
echo -e "$today $hms 3. [done] App.py 프로세스 종료 \n"
sleep 3s
ps -aux | grep app.py
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!