#!/bin/bash

source /home/iot/Documents/CNS/cns_script_header.sh

#=============================
# 7. 각 워크스테이션의 감지로그를 Azure DB로 전송하는 프로그램을 수행한다.
echo "7. [start] send detected log to Azure SQL"
python iot_detect_export.py  $linenumber $yesterday # comment : need parameters    MB3 20210811 # python iot_detect_export.py mb5 20210822
echo "7. [done] send detected log to Azure SQL"
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!