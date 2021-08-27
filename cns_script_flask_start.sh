#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 4. App.pyy 프로세스 실행 - A 이면 app.py 실행
echo -e "\n4. [start] run flask app.py"
if [ x$app == x$a ]; then
    echo "yes flask running server !!!"
    #/home/iot/anaconda3/bin/python $homedir/app.py &
    echo $SUDOPW | sudo -S chmod 777 /dev/ttyUSB0
    echo $SUDOPW | sudo -S systemctl start plotter_runner
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
echo -e "4 [done] run flask app.py \n"
ps -aux | grep app.py
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
