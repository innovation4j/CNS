#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 1회/Day 00:00:00 | S3 > S2 > S1 > R1(Top) > R2(Top) > B1 > R3
$shomedir/detection_stop.sh         &>> $lhomedir/cns_script_log_$sln$app"_"$today.out  # 1. S3: Process Stop
$shomedir/rpi_power_off.sh          &>> $lhomedir/cns_script_log_$sln$app"_"$today.out  # 2. S2: Raspberry stop - Top
$shomedir/flask_stop.sh             &>> $lhomedir/cns_script_log_$sln$app"_"$today.out  # 3. S1: Flask stop - Top
$shomedir/flask_start.sh            &>> $lhomedir/cns_script_log_$sln$app"_"$today.out  # 4. R1: Flask Start - Top
$shomedir/rpi_power_on.sh           &>> $lhomedir/cns_script_log_$sln$app"_"$today.out  # 5. R2: Raspberry Start - Top
$shomedir/move_to_export_temp.sh    &>> $lhomedir/cns_script_log_$sln$app"_"$today.out  # 6. B1: Bakcup to export_temp
$shomedir/detection_start.sh        &>> $lhomedir/cns_script_log_$sln$app"_"$today.out  # 7. R3: Process Start

$shomedir/send_file_to_nas.sh       >> $llhomedir/cns_script_log_$today.out # A2: NAS Copy
#$shomedir/delete_temp_file.sh      # A3: Delete -2 Day temp file

#$shomedir/detection_restart.sh
#$shomedir/header.sh
#$shomedir/log
#$shomedir/rpi_check.sh
#$shomedir/rpi_restart.sh


#2021-08-26 23:40 : NB3-11 에서 cns_script 정상동작 확인 함 (#표시된것 제외)