#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 1회/Hour xx:00:00 | A1
$shomedir/send_log_to_azure.sh  &>> $lhomedir/cns_script_log_$sln$app_$today.out    # A1: Export Azure - log
$shomedir/send_img_to_azure.sh  &>> $lhomedir/cns_script_log_$sln$app_$today.out    # A1: Export Azure - image