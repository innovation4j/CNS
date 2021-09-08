#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 8. cns_script_delete_temp_file
echo -e "\n$today $hms [start] delete_temp_file.sh"

function get_srccount() {
    rsync -avr --dry-run --stats $src/* $dst | 
      fgrep 'Number of files' | 
      cut -d' ' -f4 | 
      tr -d ,
}

function get_dstcount() {
    rsync -avr --dry-run --stats $dst/* $src | 
      fgrep 'Number of files' | 
      cut -d' ' -f4 | 
      tr -d , 
}

function compare_imgcount() {
    src=$homedir/export_temp/image_storage/$sln"_"$stb/$twodaysago
    dst=cns3.iptime.org::backup/01.CNS_Image_Storage/$sln"_"$stb/$twodaysago
    img_srccount=`get_srccount`
    img_dstcount=`get_dstcount`
    #echo img_srccount=$img_srccount
    #echo img_dstcount=$img_dstcount
    if [ $img_dstcount -ge $img_srccount ]; then
        echo 1
    else
        echo 0
    fi
}
function compare_logcount() {
    src=$homedir/export_temp/logs/$sln"_"$stb/$twodaysago
    dst=cns3.iptime.org::backup/01.CNS_Logs/$sln"_"$stb/$twodaysago
    log_srccount=`get_srccount`
    log_dstcount=`get_dstcount`
    #echo log_srccount=$log_srccount
    #echo log_dstcount=$log_dstcount
    if [ $log_dstcount -ge $log_srccount ]; then
        echo 1
    else
        echo 0
    fi
}


for var in {1..5} ; do
    compare_imgcount=`compare_imgcount`
    echo -e "$today $hms compare_imgcount=$compare_imgcount"
    echo -e "$today $hms run count: "$var
    if [ $compare_imgcount -eq 1 ]; then
        echo -e "$today $hms run delete yesterday image in export_temp"
        echo -e $today $hms rm -rf $homedir/export_temp/image_storage/$sln"_"$stb/$twodaysago
        rm -rf $homedir/export_temp/image_storage/$sln"_"$stb/$twodaysago
        break
    else
        echo "run send file to nas"
        $shomedir/send_file_to_nas.sh       &>> $lhomedir/log_$today"_"1day.log  # A2: NAS Copy
    fi
done

for var in {1..5} ; do
    compare_logcount=`compare_logcount`
    echo -e "$today $hms compare_logcount=$compare_logcount"
    echo -e "$today $hms run count: "$var
    if [ $compare_logcount -eq 1 ]; then
        echo -e "$today $hms run delete yesterday log in export_temp"
        echo -e $today $hms rm -rf $homedir/export_temp/logs/$sln"_"$stb/$twodaysago
        rm -rf $homedir/export_temp/logs/$sln"_"$stb/$twodaysago
        break
    else
        echo -e "$today $hms run send file to nas"
        $shomedir/send_file_to_nas.sh       &>> $lhomedir/log_$today"_"1day.log  # A2: NAS Copy
    fi
done


echo -e "$today $hms [done] delete_temp_file.sh \n"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!