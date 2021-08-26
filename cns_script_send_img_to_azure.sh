#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 6. 각 워크스테이션의 하루전날 감지이미지를 Azure Storage로 옮긴다. 원본삭제
echo "6. [start] move detected image to Azure blob"
# rclone copy $homedir/image_storage/mb4/detection/ remote:\$web/mb4  <== 이것만 적용됨
src="$homedir/export_temp/image_storage/$linenumber/$yesterday/detection/"
dst="remote:\$web/$lln/$yesterday"
rclone copy $src $dst
##rclone delete remote:\$web/$linenumber
#rm -rf $src*
echo "6. [done] move detected image to Azure blob"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!