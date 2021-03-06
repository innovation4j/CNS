#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# [RPI Running Check]. 각 라즈베리 스트림 서비스 체크, 전체스트림서비스 동작 확인되면 다음으로 진행 아니면 2분 추가 sleep
# PRD
echo -e "\n$today $hms [start] rpi_check.sh"
url="https://hooks.slack.com/services/................."
websites_list=""
for var in {1..7} ; do
    tempurl="http://192.168.0.$lineip$var:8080/?action=stream"
    websites_list+=$tempurl" "
done

# 배열 key값으로 index를 활용. 파일생성명
cnt=0
rp_status=0
rp_status_result=0
check_rp_status()
{
for website in ${websites_list} ; do
    status_code=$(curl --write-out %{http_code} --silent --output ./ -L ${website})
    # 웹 서버 장애인경우
    if [[ "$status_code" -ne 200 ]] ; then
        break
    # 웹 서버 장애가 아닌경우
    else
        rp_status=1
    fi
    # 지연시간 추가
    sleep 0.01s
done
echo $rp_status
}
#=============================

while :
do
rp_status_result=`check_rp_status`
#echo $rp_status_result
    if [ $rp_status_result -eq 1 ] ; then
        echo "$today $hms RPIs are up"
        break
    else
        rp_status_result=`check_rp_status`
        echo "$today $hms RPIs are down"
        sleep 1s
    fi    
    echo $rp_status_result
done
echo -e "$today $hms [done] rpi_check.sh \n"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!