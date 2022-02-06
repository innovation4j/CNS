import pymssql
import sys

if len(sys.argv) == 4:
    inputArr = sys.argv
    equipmentId = inputArr[1]
    today = inputArr[2]
    stb = inputArr[3]

    conn = pymssql.connect(host='cnssql01.database.windows.net', user='cnsadmin', password='MMSupp0rt2021', database='predict01')
    # Connection 으로부터 Cursor 생성
    cursor = conn.cursor()

    f = open(f"/home/iot/Documents/CNS/export_temp/logs/{equipmentId}_{stb}/{str(today)[:8]}/EXP/{today}_{equipmentId}_EXP.log", 'r') #'/mb5/20210830/EXP/20210830_mb5_EXP.log' 
    
    while True:
        line = f.readline()
        if not line: break
        print(line)
        lineList = line.rstrip('\n').split('|')
        print(lineList)
        sql = "INSERT INTO MM_DETECT_INFO(WORK_CENTER,CAM_NO,D_DATE,D_TIME,PRED_SCORE,OBJECT_SIZE,OBJECT_AXIS,IMAGE_NAME,CREATE_DTIME, PRINT_YN, SWITCH_ONOFF) VALUES ('"+lineList[0]+"','"+lineList[1]+"','"+lineList[2]+"','"+lineList[3]+"','"+lineList[4]+"','"+lineList[5]+"','"+lineList[6]+"',trim('"+lineList[7]+"'), dateadd(hour, 9, getdate()), '"+lineList[8]+"', '"+lineList[9]+"')"
        print(sql)
        cursor.execute( sql )

    conn.commit()
    conn.close()
    f.close()

else:
    print(f'input argv error')






 