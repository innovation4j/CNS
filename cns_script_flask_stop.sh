#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 3. App.py 프로세스 종료
echo -e "\n3. [start] App.py 프로세스 종료"
if [ x$app == x$a ]; then
    echo "yes flask running server !!!"
    #sudo ps -ef | grep app.py | awk '{print $2}' | xargs kill -9
    echo $SUDOPW | sudo -S systemctl stop plotter_runner
else
    echo "no flask running server !!!"
    echo "wait 10 seconds !!!"
    SET=$(seq 1 10)
    for i in $SET
    do
        sleep 1s
        echo "$i s"
    done
fi
sleep 3s
echo -e "3. [done] App.py 프로세스 종료 \n"
ps -aux | grep app.py
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!