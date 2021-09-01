#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 3. App.py 프로세스 종료
echo -e "\n$today $hms [start] flask_stop.sh"
if [ x$app == x$a ]; then
    echo "$today $hms yes flask running server !!!"
    #sudo ps -ef | grep app.py | awk '{print $2}' | xargs kill -9
    echo "$today $hms XXXXXX | sudo -S systemctl stop plotter_runner"
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
echo -e "$today $hms [done] flask_stop.sh \n"
sleep 3s
ps -aux | grep app.py
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!