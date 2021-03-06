#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 1회/Day 00:00:00 | S3 > S2 > S1 > R1(Top) > R2(Top) > B1 > R3
$shomedir/detection_stop.sh         &>> $lhomedir/log_$today"_"1day.log  # 1. S3: Process Stop
$shomedir/rpi_power_off.sh          &>> $lhomedir/log_$today"_"1day.log  # 2. S2: Raspberry stop - Top
$shomedir/flask_stop.sh             &>> $lhomedir/log_$today"_"1day.log  # 3. S1: Flask stop - Top
$shomedir/flask_start.sh            &>> $lhomedir/log_$today"_"1day.log  # 4. R1: Flask Start - Top
$shomedir/rpi_power_on.sh           &>> $lhomedir/log_$today"_"1day.log  # 5. R2: Raspberry Start - Top
$shomedir/move_to_export_temp.sh    &>> $lhomedir/log_$today"_"1day.log  # 6. B1: Bakcup to export_temp
$shomedir/detection_start.sh        &>> $lhomedir/log_$today"_"1day.log  # 7. R3: Process Start

$shomedir/send_file_to_nas.sh       &>> $lhomedir/log_$today"_"1day.log  # A2: NAS Copy
$shomedir/delete_temp_file.sh       &>> $lhomedir/log_$today"_"1day.log  # A3: Delete -2 Day temp file

#$shomedir/detection_restart.sh
#$shomedir/header.sh
#$shomedir/log
#$shomedir/rpi_check.sh
#$shomedir/rpi_restart.sh
