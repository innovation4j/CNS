#!/bin/bash

hostnamecut=${HOSTNAME:3:3}
#echo hostnamecut=$hostnamecut
linenumber=${hostnamecut,,}
#echo linenumber=$linenumber
lln=`echo $linenumber | tr '[a-z]' '[A-Z]'`
#echo lln=$lln
sln=`echo $linenumber | tr '[A-Z]' '[a-z]'`
#echo sln=$sln
homedir="/home/iot/Documents/CNS"
#echo homedir=$homedir
shomedir="/home/iot/Documents/CNS/cns_script"
#echo shomedir=$shomedir
lhomedir="/home/iot/Documents/CNS/cns_script_log"
#echo lhomedir=$lhomedir
today=$(date "+%Y%m%d")
#echo today=$today
yesterday=$(date -d yesterday +%Y%m%d)
#echo yesterday=$yesterday
twodaysago=$(date '+%Y%m%d' -d '2 days ago')
#echo twodaysago=$twodaysago
hms=$(date "+%H%M%S")
#echo hms=$hms


#서버이름변경 명령어
#sudo hostnamectl set-hostname CNSMB4-14BTMX
#라인번호를 ip 4번째자리 시작번호로 할당하기위한 변수
lineip=${HOSTNAME:5:1}
#echo lineip=$lineip

#상단, 하단 구분 컴퓨터이름 TOP, BTM
tb=${HOSTNAME:9:3}

tb2=${HOSTNAME:9:2}

if [ "$tb2" == "bt" ]; then
    stb="btm"
elif [ "$tb2" == "BT" ]; then
    stb="btm"
else 
    stb="top"
fi

top="TOP"
btm="BTM"
bt1="bt1"
bt2="bt2"

#app.py 실행서버 구분
app=${HOSTNAME:12:1}
a="A"
x="X"
#echo app=$app, a=$a