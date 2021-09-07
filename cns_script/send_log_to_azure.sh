#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh


#=============================
# 7. 각 워크스테이션의 감지로그를 Azure DB로 전송하는 프로그램을 수행한다.
echo -e "\n$today $hms [start] send_log_to_azure.sh"
echo /home/iot/anaconda3/bin/python "$homedir"/iot_detect_export.py $linenumber $today
/home/iot/anaconda3/bin/python "$homedir"/iot_detect_export.py $linenumber $today # comment : need parameters MB5 20210811
src="$homedir"/logs/"$linenumber"/"$today"/EXP/"$today"_"$linenumber"_EXP.log
dst="$homedir"/logs/"$linenumber"/"$today"/EXP/"$today"_"$hms"_"$linenumber"_EXP.log
mv $src $dst
echo $today $hms mv $src $dst
echo -e "$today $hms [done] send_log_to_azure.sh \n"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!