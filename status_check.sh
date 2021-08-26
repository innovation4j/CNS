#!/bin/bash

hostnamecut=${HOSTNAME:3:3}
echo hostnamecut=$hostnamecut
linenumber=${hostnamecut,,}
echo linenumber=$linenumber
homedir="/home/iot/Documents/CNS"
echo homedir=$homedir
today=$(date "+%Y%m%d")
echo today=$today


#서버이름변경 명령어
#sudo hostnamectl set-hostname CNSMB4-14BTMX
a
#라인번호를 ip 4번째자리 시작번호로 할당하기위한 변수
lineip=${HOSTNAME:5:1}
echo lineip=$lineip

#상단, 하단 구분 컴퓨터이름 끝자리를 2로 나눠 나머지가 1이면 상단, 0이면 하단
#tb=`echo ${HOSTNAME:11:1}%2 | bc`
#echo $tb

#상단, 하단 구분 컴퓨터이름 TOP, BTM
tb=${HOSTNAME:9:3}
top="TOP"
btm="BTM"
echo tb=$tb, top=$top

#app.py 실행서버 구분
app=${HOSTNAME:12:1}
a="A"
x="X"
echo app=$app, a=$a


#=============================
# 1. cns_detection.py 프로세스를 전부 종료
echo "1. [start] kill cns_detection.py"
pkill -9 -ef cns_detection.py
echo"pkill -9 -ef cns_detection.py"
echo "1. [done] kill cns_detection.py"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 2. 라즈베리를 전체 리스타트
echo "2. [start] restart raspberry pi"
#curl http://192.168.0.13:5000/reset
# A 이면 라즈베리를 전체 리스타트 실행
if [ x$app == x$a ]; then
    curl http://127.0.0.1:5000/reset
    echo "curl http://127.0.0.1:5000/reset"
else
    echo="no app.py running server"
fi
echo "2. [done] restart raspberry pi"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 2-1. 라즈베리 전체 전원 off
echo "2-1. [start] power off all raspberry pi"
#curl http://192.168.0.13:5000/reset
# A 라즈베리 전체 전원 Off
if [ x$app == x$a ]; then
    curl http://127.0.0.1:5000/rasoff
    echo "curl http://127.0.0.1:5000/rasoff"
else
    echo="no app.py running server"
fi
echo "2-1. [done] power off all raspberry pi"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 2-2. 라즈베리 전체 전원 On
echo "2-1. [start] power on all raspberry pi"
# A 이면 라즈베리 전체 전원 On
if [ x$app == x$a ]; then
    curl http://127.0.0.1:5000/rason
    echo "curl http://127.0.0.1:5000/rason"
else
    echo="no app.py running server"
fi
echo "2-1. [done] power on all raspberry pi"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 3. 리셋 완료까지 2분 가량 sleep
echo "3. [start] sleep 120s"
sleep 1s
echo "sleep 1s"
echo "3. [done] sleep 120s"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#=============================
# 4. 각 라즈베리 스트림 서비스 체크, 전체스트림서비스 동작 확인되면 다음으로 진행 아니면 2분 추가 sleep
# PRD
echo "4. [start] check restart raspberry pi"
url="https://hooks.slack.com/services/................."
websites_list=""
for var in {1..7} ; do
    tempurl="http://192.168.0.$lineip$var:8080/?action=stream"
    echo "$tempurl"
    websites_list+=$tempurl" "
    echo "$websites_list"
done
#echo $websites_list

# 배열 key값으로 index를 활용. 파일생성명
cnt=0
rp_status=0
rp_status_result=0
check_rp_status()
{
for website in ${websites_list} ; do
    #파일명 생성
    #file_check=${file_prefix}${cnt}${file_realfix}
    #echo "filecheck" $file_check

    # CORE
    #status_code=$(curl --write-out %{http_code} --silent --output /dev/null -L ${website})
    status_code=$(curl --write-out %{http_code} --silent --output ./ -L ${website})
    echo "status_code=$status_code"
    # 웹 서버 장애인경우
    if [[ "$status_code" -ne 200 ]] ; then
        #echo "${website} is stil failed!"
        rp_status=0
        echo "rp_status=0"
        break        
        echo "break"
    # 웹 서버 장애가 아닌경우
    else
        #echo "${website} is running!"
        rp_status=1
        echo "rp_status=1"
    fi
    # 지연시간 추가
    sleep 0.01s
done
echo $rp_status
}
#=============================
#rp_status_result=`check_rp_status`
#echo "rp_status_result = "$rp_status_result
while :
do
rp_status_result=`check_rp_status`
    if [ $rp_status_result -eq 1 ] ; then
        echo "RPIs are up"
        break
    else
        rp_status_result=`check_rp_status`
        echo "RPIs are down"
        sleep 5s
    fi    
    echo $rp_status_result
done
echo "4. [done] check restart raspberry pi"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 5. App.py 프로세스 종료
echo "5. [start] App.py 프로세스 종료"
#sudo ps -ef | grep app.py | awk '{print $2}' | xargs kill -9
echo $SUDOPW | sudo -S systemctl stop plotter_runner
echo "$SUDOPW | sudo -S systemctl stop plotter_runner"
echo "5. [done] App.py 프로세스 종료"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 6. 각 워크스테이션의 감지이미지를 Azure Storage로 옮긴다. 원본삭제
echo "6. [start] move detected image to Azure blob"
# rclone copy $homedir/image_storage/mb4/detection/ remote:\$web/mb4  <== 이것만 적용됨
src="$homedir/image_storage/$linenumber/detection/"
dst="remote:\$web/$linenumber"
rclone copy $src $dst
##rclone delete remote:\$web/$linenumber
#rm -rf $src*
echo "6. [done] move detected image to Azure blob"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 7. 각 워크스테이션의 감지로그를 Azure DB로 전송하는 프로그램을 수행한다.
echo "7. [start] send detected log to Azure SQL"
python iot_detect_export.py  # comment : need parameters    MB3 20210811
echo "7. [done] send detected log to Azure SQL"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 8. 각 워크스테이션에 이미지를 NAS로 옮긴다. 원본삭제
echo "8. [start] send image to NAS"
src2="$homedir/image_storage/$linenumber/"
dst2="cns3.iptime.org::backup/01.CNS_Image_Storage/$linenumber"
rsync -avr --exclude="detection" $src2 $dst2
##rclone delete remote:\$web/$linenumber
##rm -rf `ls | find $homedir/image_storage/mb4/* -name detection -prune -o -print`
#rm -rf `ls | find $src2* -name detection -prune -o -print`
echo "8. [done] send image to NAS"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 9. 각 워크스테이션의 로그를 NAS로 옮긴다. 원본삭제
echo "9. [start] send detected log to NAS"
src3="$homedir/logs/$linenumber/"
dst3="cns3.iptime.org::backup/01.CNS_Logs/$linenumber"
rsync -avr --exclude="detection" $src3 $dst3
##rclone delete remote:\$web/$linenumber
##rm -rf `ls | find $homedir/image_storage/mb4/* -name detection -prune -o -print`
#rm -rf `ls | find $src3* -name detection -prune -o -print`
echo "9 [done] send detected log to NAS"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 10. App.pyy 프로세스 실행 - A 이면 app.py 실행
echo "10. [start] run app.py"
if [ x$ax == x$a ]; then
    #/home/iot/anaconda3/bin/python $homedir/app.py &
    echo $SUDOPW | sudo -S chmod 777 /dev/ttyUSB0
    echo $SUDOPW | sudo -S systemctl start plotter_runner
else
    echo="no app.py running server"
fi
echo "10 [done] run app.py"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 11. cns_detection.py 프로세스 실행
echo "11. [start] run cns_detection.py"
# top 이면 cns_dection.py x1, x2, x3 실행
if [ x$tb == x$top ]; then
    for var in {1..3} ; do
        #/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var
        #tmp="/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var"
        #echo $tmp
        echo $SUDOPW | sudo -S systemctl start cns_detection_$lineip$var
    done
# bottom 이면 cns_dection.py x4, x5, x6, x7 실행
elif [ x$tb == x$btm ]; then
    for var in {4..7} ; do
        #/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var
        #tmp="/home/iot/anaconda3/bin/python $homedir/cns_detection.py $linenumber 50 2000 $lineip$var"
        #echo $tmp
        echo $SUDOPW | sudo -S systemctl start cns_detection_$lineip$var
    done
fi
echo "11 [done] run cns_detection.py"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!