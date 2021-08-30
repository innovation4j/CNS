#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh


#=============================
# 7. 각 워크스테이션의 감지로그를 Azure DB로 전송하는 프로그램을 수행한다.
echo "7. [start] send detected log to Azure SQL"
python /home/iot/Documents/CNS/iot_detect_export.py $linenumber $today # comment : need parameters MB5 20210811
mv "$homedir"/logs/"$linenumber"/"$today"/EXP/"$today"_"$linenumber"_EXP.log "$homedir"/logs/"$linenumber"/"$today"_$hms/EXP/"$today"_"$linenumber"_EXP.log
echo mv "$homedir"/logs/"$linenumber"/"$today"/EXP/"$today"_"$linenumber"_EXP.log "$homedir"/logs/"$linenumber"/"$today"_$hms/EXP/"$today"_"$linenumber"_EXP.log
echo "7. [done] send detected log to Azure SQL"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!