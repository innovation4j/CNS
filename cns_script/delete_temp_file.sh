#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 8. cns_script_delete_temp_file
echo -e "\n$today $hms [start] delete_temp_file.sh"

src="$homedir/export_temp/image_storage/$sln/$twodaysago"
dst="cns3.iptime.org::backup/01.CNS_Image_Storage/$sln/$twodaysago"
#rsync -avr $src2 $dst2

echo -e "$today $hms [done] delete_temp_file.sh \n"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!