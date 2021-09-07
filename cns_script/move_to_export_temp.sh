#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 6. 각 워크스테이션의 하루전날 이미지와 로그를 export_temp로 옮긴다.
echo -e "\n$today $hms [start] move_to_export_temp.sh"

src1="$homedir/image_storage/*"
dst1="$homedir/export_temp/image_storage/"
#오늘날짜 image 제외 전체 동기화 to export_temp
echo "$today $hms rsync -a --exclude="$today" $src1 $dst1"
rsync -a --exclude="$today" $src1 $dst1
#오늘날짜 image 제외 전체 삭제 in image_storage 폴더
echo "$today $hms rm -rf 'ls | find $homedir/image_storage/$sln"_"$stb/* -name $today -prune -o -print'"
rm -rf `ls | find $homedir/image_storage/$sln"_"$stb/* -name $today -prune -o -print`

src2="$homedir/logs/*"
dst2="$homedir/export_temp/logs/"
#오늘날짜 log 제외 전체 동기화 to export_temp
echo "$today $hms rsync -a --exclude=$today $src2 $dst2"
rsync -a --exclude="$today" $src2 $dst2
#오늘날짜 log 제외 전체 삭제 in logs 폴더
echo "$today $hms rm -rf 'ls | find $homedir/logs/$sln"_"$stb/* -name $today -prune -o -print'"
rm -rf `ls | find $homedir/logs/$sln"_"$stb/* -name $today -prune -o -print`

echo -e "$today $hms [done] move_to_export_temp.sh \n"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!