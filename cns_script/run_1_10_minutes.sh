#!/bin/bash

source /home/iot/Documents/CNS/cns_script/header.sh

#=============================
# 1회/Hour xx:00:00 | A1
$shomedir/send_log_to_azure.sh  &>> $lhomedir/log_$today"_"10min.log    # A1: Export Azure - log
$shomedir/send_img_to_azure.sh  &>> $lhomedir/log_$today"_"10min.log    # A1: Export Azure - image
