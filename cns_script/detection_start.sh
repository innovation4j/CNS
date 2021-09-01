#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 7. cns_detection.py 프로세스 실행
echo -e "\n$today $hms [start] detection_start.sh"
# top 이면 cns_dection.py x1, x2, x3 실행
if [ x$tb == x$top ]; then
    for var in {1..3} ; do
        #/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var
        #tmp="/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var"
        #echo $tmp
        echo "$today $hms XXXXXX | sudo -S systemctl start cns_detection_$lineip$var"
        echo $SUDOPW | sudo -S systemctl start cns_detection_$lineip$var
    done
# bottom 이면 cns_dection.py x4, x5, x6, x7 실행
elif [ x$tb == x$btm ]; then
    for var in {4..7} ; do
        #/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var
        #tmp="/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var"
        #echo $tmp
        echo "$today $hms XXXXXX | sudo -S systemctl start cns_detection_$lineip$var"
        echo $SUDOPW | sudo -S systemctl start cns_detection_$lineip$var
    done
fi
echo -e "$today $hms [done] detection_start.sh \n"
sleep 3s
ps -aux | grep cns
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!