#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 11. cns_detection.py 프로세스 실행
echo -e "\n$today $hms [start] detection_restart.sh"
# top 이면 cns_dection.py x1, x2, x3 실행
if [ x$tb == x$top ]; then
    for var in {1..3} ; do
        #/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var
        #tmp="/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var"
        #echo $tmp
        echo "$today $hms XXXXXX | sudo -S systemctl restart cns_detection_$lineip$var"
        echo $SUDOPW | sudo -S systemctl restart cns_detection_$lineip$var
    done
# bottom 이면 cns_dection.py x4, x5, x6, x7 실행
elif [ x$tb == x$btm ]; then
    for var in {4..7} ; do
        #/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var
        #tmp="/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var"
        #echo $tmp
        echo "$today $hms XXXXXX | sudo -S systemctl restart cns_detection_$lineip$var"
        echo $SUDOPW | sudo -S systemctl restart cns_detection_$lineip$var
    done
# bottom1 이면 cns_dection.py x4, x5 실행
elif [ x$tb == x$bt1 ]; then
    for var in {4..5} ; do
        #/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var
        #tmp="/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var"
        #echo $tmp
        echo "$today $hms XXXXXX | sudo -S systemctl restart cns_detection_$lineip$var"
        echo $SUDOPW | sudo -S systemctl restart cns_detection_$lineip$var
    done
# bottom2 이면 cns_dection.py x6, x7 실행
elif [ x$tb == x$bt2 ]; then
    for var in {6..7} ; do
        #/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var
        #tmp="/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var"
        #echo $tmp
        echo "$today $hms XXXXXX | sudo -S systemctl restart cns_detection_$lineip$var"
        echo $SUDOPW | sudo -S systemctl restart cns_detection_$lineip$var
    done
fi
echo -e "$today $hms [done] detection_restart.sh \n"
sleep 3s
ps -aux | grep cns
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!