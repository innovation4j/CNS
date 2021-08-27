# 1회/Day 00:00:00 | S3 > S2 > S1 > R1(Top) > R2(Top) > B1 > R3
./cns_script_detection_stop.sh          # S3: Process Stop
./cns_script_rpi_power_off.sh           # S2: Raspberry stop - Top
./cns_script_flask_stop.sh              # S1: App.py stop - Top
./cns_script_flask_start.sh             # R1: App.py run - Top
./cns_script_rpi_power_on.sh            # R2: Raspberry run - Top
./cns_script_backup_to_export_temp.sh   # B1: Bakcup to export_temp
./cns_script_detection_start.sh         # R3: Process run

# 1회/Hour xx:00:00 | A1
./cns_script_send_img_to_azure.sh       # A1: Export Azure - image
#./cns_script_send_log_to_azure.sh      # A1: Export Azure - log
# DB에 중복으로 입력 됨

./cns_script_send_file_to_nas.sh         # A2: NAS Copy
#./cns_script_delete_temp_file.sh        # A3: Delete -2 Day temp file

#./cns_script_detection_restart.sh
#./cns_script_header.sh
#./cns_script_log
#./cns_script_rpi_check.sh
#./cns_script_rpi_restart.sh


#2021-08-26 23:40 : NB3-11 에서 cns_script 정상동작 확인 함 (#표시된것 제외)