#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 각 워크스테이션의 하루전날 이미지와 로그를 export_temp로 옮긴다.
echo "[start] move file to export_temp"
src1="$homedir/image_storage/*"
dst1="$homedir/export_temp/image_storage/"
mv $src1 $dst1

src2="$homedir/logs/*"
dst2="$homedir/export_temp/logs/"
mv $src2 $dst2
echo "[done] move file to export_temp"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!