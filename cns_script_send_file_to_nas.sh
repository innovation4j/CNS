#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 8. 각 워크스테이션에 이미지를 NAS로 옮긴다. 원본삭제
echo "8. [start] send image to NAS"
src2="$homedir/export_temp/image_storage/$linenumber/$yesterday/*"
dst2="cns3.iptime.org::backup/01.CNS_Image_Storage/$linenumber/$yesterday"
rsync -avr $src2 $dst2
#특정폴더제외 "detection"
#rsync -avr --exclude="detection" $src2 $dst2
##rclone delete remote:\$web/$linenumber
##rm -rf `ls | find $homedir/image_storage/mb4/* -name detection -prune -o -print`
#rm -rf `ls | find $src2* -name detection -prune -o -print`
echo "8. [done] send image to NAS"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#=============================
# 9. 각 워크스테이션의 로그를 NAS로 옮긴다. 원본삭제
echo "9. [start] send detected log to NAS"
src3="$homedir/export_temp/logs/$linenumber/$yesterday/*"
dst3="cns3.iptime.org::backup/01.CNS_Logs/$linenumber/$yesterday"
rsync -avr --exclude="detection" $src3 $dst3
##rclone delete remote:\$web/$linenumber
##rm -rf `ls | find $homedir/image_storage/mb4/* -name detection -prune -o -print`
#rm -rf `ls | find $src3* -name detection -prune -o -print`
echo "9 [done] send detected log to NAS"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!