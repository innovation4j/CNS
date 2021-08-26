#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 11. cns_detection.py 프로세스 실행
echo "11. [start] run cns_detection.py"
# top 이면 cns_dection.py x1, x2, x3 실행
if [ x$tb == x$top ]; then
    for var in {1..3} ; do
        #/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var
        #tmp="/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var"
        #echo $tmp
        echo $SUDOPW | sudo -S systemctl restart cns_detection_$lineip$var
    done
# bottom 이면 cns_dection.py x4, x5, x6, x7 실행
elif [ x$tb == x$btm ]; then
    for var in {4..7} ; do
        #/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var
        #tmp="/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var"
        #echo $tmp
        echo $SUDOPW | sudo -S systemctl restart cns_detection_$lineip$var
    done
fi
echo "11 [done] run cns_detection.py"
ps -aux | grep cns
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!