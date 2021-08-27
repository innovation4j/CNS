#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 6. 각 워크스테이션의 하루전날 이미지와 로그를 export_temp로 옮긴다.
echo -e "\n6. [start] move file to export_temp"
src1="$homedir/image_storage/*"
dst1="$homedir/export_temp/image_storage/"
#mv $src1 $dst1
rsync -a $src1 $dst1
rm -rf $src1

src2="$homedir/logs/*"
dst2="$homedir/export_temp/logs/"
#mv $src2 $dst2
rsync -a $src2 $dst2
rm -rf $src2
echo -e "6. [done] move file to export_temp \n"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!