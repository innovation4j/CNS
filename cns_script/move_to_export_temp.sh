#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 6. 각 워크스테이션의 하루전날 이미지와 로그를 export_temp로 옮긴다.
echo -e "\n$today $hms 6. [start] move_to_export_temp"
src1="$homedir/image_storage/*"
dst1="$homedir/export_temp/image_storage/"
#mv $src1 $dst1
echo "$today $hms rsync -a --exclude=$today $src1 $dst1"
rsync -a --exclude="$today" $src1 $dst1
echo "$today $hms rm -rf $src1"
rm -rf $src1

src2="$homedir/logs/*"
dst2="$homedir/export_temp/logs/"
#mv $src2 $dst2
echo "$today $hms rsync -a --exclude=$today $src2 $dst2"
rsync -a --exclude="$today" $src2 $dst2
echo "$today $hms rm -rf $src2"
rm -rf $src2
echo -e "$today $hms 6. [done] move_to_export_temp \n"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!