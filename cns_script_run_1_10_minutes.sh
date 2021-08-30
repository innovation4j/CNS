# 1회/Day 00:00:00 | S3 > S2 > S1 > R1(Top) > R2(Top) > B1 > R3
#/home/iot/Documents/CNS/cns_script_detection_stop.sh        # 1. S3: Process Stop
#/home/iot/Documents/CNS/cns_script_rpi_power_off.sh         # 2. S2: Raspberry stop - Top
#/home/iot/Documents/CNS/cns_script_flask_stop.sh            # 3. S1: Flask stop - Top
#/home/iot/Documents/CNS/cns_script_flask_start.sh           # 4. R1: Flask Start - Top
#/home/iot/Documents/CNS/cns_script_rpi_power_on.sh          # 5. R2: Raspberry Start - Top
#/home/iot/Documents/CNS/cns_script_backup_to_export_temp.sh # 6. B1: Bakcup to export_temp
#/home/iot/Documents/CNS/cns_script_detection_start.sh       # 7. R3: Process Start

# 1회/Hour xx:00:00 | A1
/home/iot/Documents/CNS/cns_script_send_img_to_azure.sh     # A1: Export Azure - image
/home/iot/Documents/CNS/cns_script_send_log_to_azure.sh     # A1: Export Azure - log

#/home/iot/Documents/CNS/cns_script_send_file_to_nas.sh      # A2: NAS Copy
#/home/iot/Documents/CNS/cns_script_delete_temp_file.sh      # A3: Delete -2 Day temp file

#/home/iot/Documents/CNS/cns_script_detection_restart.sh
#/home/iot/Documents/CNS/cns_script_header.sh
#/home/iot/Documents/CNS/cns_script_log
#/home/iot/Documents/CNS/cns_script_rpi_check.sh
#/home/iot/Documents/CNS/cns_script_rpi_restart.sh


#2021-08-26 23:40 : NB3-11 에서 cns_script 정상동작 확인 함 (#표시된것 제외)