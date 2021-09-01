#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 4. App.pyy 프로세스 실행 - A 이면 app.py 실행
echo -e "\n$today $hms [start] run flask app.py"
if [ x$app == x$a ]; then
    echo "$today $hms yes flask running server !!!"
    #/home/iot/anaconda3/bin/python $homedir/app.py &
    echo "$today $hms XXXXXX | sudo -S chmod 777 /dev/ttyUSB0"
    echo $SUDOPW | sudo -S chmod 777 /dev/ttyUSB0
    echo "$today $hms XXXXXX | ssystemctl start plotter_runner"
    echo $SUDOPW | sudo -S systemctl start plotter_runner
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
echo -e "$today $hms [done] flask_start.sh \n"
sleep 3s
ps -aux | grep app.py
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
