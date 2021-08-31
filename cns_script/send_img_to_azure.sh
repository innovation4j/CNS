#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 6. 각 워크스테이션의 하루전날 감지이미지를 Azure Storage로 옮긴다. 원본삭제
echo "6. [start] copy detected image to Azure blob"
# rclone copy $homedir/image_storage/mb4/detection/ remote:\$web/mb4  <== 이것만 적용됨
src="$homedir/export_temp/image_storage/$linenumber/$yesterday/detection/"
dst="remote:\$web/$lln/$yesterday"
echo -e "\n--copy start for yesterday $yesterday detected images in temp"
echo -e "rclone copy $src $dst"
rclone copy $src $dst
echo -e "--copy done for yesterday $yesterday detected images in temp \n"

src="$homedir/export_temp/image_storage/$linenumber/$today/detection/"
dst="remote:\$web/$lln/$today"
echo -e "\n--copy start for today $today detected images in temp"
echo -e "rclone copy $src $dst"
rclone copy $src $dst
echo -e "--copy done for today $yesterday detected images in temp \n"

src3="$homedir/image_storage/$linenumber/$today/detection/"
dst3="remote:\$web/$lln/$today"
echo -e "\n--copy start for today $today detected images"
echo -e "rclone copy $src3 $dst3"
rclone copy $src3 $dst3
echo -e "-copy done for today $today detected images \n"

##rclone delete remote:\$web/$linenumber
#rm -rf $src*
echo "6. [done] copy detected image to Azure blob"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!