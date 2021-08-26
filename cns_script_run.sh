./cns_script_detection_stop.sh
./cns_script_rpi_power_off.sh
./cns_script_flask_stop.sh
sleep 5s
./cns_script_flask_start.sh
./cns_script_rpi_power_on.sh

./cns_script_backup_to_export_temp.sh

./cns_script_detection_start.sh

./cns_script_send_img_to_azure.sh
#./cns_script_send_log_to_azure.sh
./cns_script_send_file_to_nas.sh
#./cns_script_delete_temp_file.sh

#./cns_script_detection_restart.sh
#./cns_script_header.sh
#./cns_script_log
#./cns_script_rpi_check.sh
#./cns_script_rpi_restart.sh


#2021-08-26 23:40 : NB3-11 에서 cns_script 정상동작 확인 함 (#표시된것 제외)