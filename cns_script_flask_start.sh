#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 10. App.pyy 프로세스 실행 - A 이면 app.py 실행
echo "10. [start] run app.py"
if [ x$app == x$a ]; then
    #/home/iot/anaconda3/bin/python $homedir/app.py &
    echo $SUDOPW | sudo -S chmod 777 /dev/ttyUSB0
    echo $SUDOPW | sudo -S systemctl start plotter_runner
else
    echo="no app.py running server"
fi
echo "10 [done] run app.py"
ps -aux | grep app.py
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
