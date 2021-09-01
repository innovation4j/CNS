import os

# 현재 파일 경로 및 파일명 찾기

    

def setSource(eqpt, id):
    source = ("", "")
    print_ip = "http://127.0.0.1:5000"
    if eqpt == "mb3":
        print_ip = 'http://192.168.0.11:5000'
        if id==31:
            source = ("t1", "http://192.168.0.31:8080/?action=stream")
        if id==32:
            source = ("t2", "http://192.168.0.32:8080/?action=stream")
        if id==33:
            source = ("t3", "http://192.168.0.33:8080/?action=stream")
        if id==34:
            source = ("b1", "http://192.168.0.34:8080/?action=stream")
        if id==35:
            source = ("b2", "http://192.168.0.35:8080/?action=stream")
        if id==36:
            source = ("b3", "http://192.168.0.36:8080/?action=stream")
        if id==37:
            source = ("b4", "http://192.168.0.37:8080/?action=stream")
    
    if eqpt == "mb4":
        print_ip = "http://192.168.0.13:5000"
        if id==41:
            source = ("t1", "http://192.168.0.41:8080/?action=stream")
        if id==42:
            source = ("t2", "http://192.168.0.42:8080/?action=stream")
        if id==43:
            source = ("t3", "http://192.168.0.43:8080/?action=stream")
        if id==44:
            source = ("b1", "http://192.168.0.44:8080/?action=stream")
        if id==45:
            source = ("b2", "http://192.168.0.45:8080/?action=stream")
        if id==46:
            source = ("b3", "http://192.168.0.46:8080/?action=stream")
        if id==47:
            source = ("b4", "http://192.168.0.47:8080/?action=stream")

    if eqpt == "mb5":
        print_ip = "http://192.168.0.16:5000"
        if id==51:
            source = ("t1", "http://192.168.0.51:8080/?action=stream")
        if id==52:
            source = ("t2", "http://192.168.0.52:8080/?action=stream")
        if id==53:
            source = ("t3", "http://192.168.0.53:8080/?action=stream")
        if id==54:
            source = ("b1", "http://192.168.0.54:8080/?action=stream")
        if id==55:
            source = ("b2", "http://192.168.0.55:8080/?action=stream")
        if id==56:
            source = ("b3", "http://192.168.0.56:8080/?action=stream")
        if id==57:
            source = ("b4", "http://192.168.0.57:8080/?action=stream")

    if eqpt == "mb6":
        print_ip = "http://192.168.0.17:5000"
        if id==61:
            source = ("t1", "http://192.168.0.61:8080/?action=stream")
        if id==62:
            source = ("t2", "http://192.168.0.62:8080/?action=stream")
        if id==63:
            source = ("t3", "http://192.168.0.63:8080/?action=stream")
        if id==64:
            source = ("b1", "http://192.168.0.64:8080/?action=stream")
        if id==65:
            source = ("b2", "http://192.168.0.65:8080/?action=stream")
        if id==66:
            source = ("b3", "http://192.168.0.66:8080/?action=stream")
        if id==67:
            source = ("b4", "http://192.168.0.67:8080/?action=stream")
    return source, print_ip


def setValue(eqpt, id):
    #settingValue (x축시작좌표(mm), X축 변환값(px->mm), Y축 변환값(px->mm), x축 범위최소값, x축 범위 최대값)
    value = (0, 0, 0, 0, 0)
    id = id%10
    if eqpt == "mb3":
        if id==1:
            value = (0, 0.31, 0.31, 0, 1920)
        if id==2:
            value = (600, 0.31, 0.31, 0, 1920)
        if id==3:
            value = (1200, 0.31, 0.31, 0, 1920)
        if id==4:
            value = (0, 0.23, 0.23, 0, 1920)
        if id==5:
            value = (450, 0.23, 0.23, 0, 1920)
        if id==6:
            value = (900, 0.23, 0.23, 0, 1920)  
        if id==7:
            value = (1350, 0.23, 0.23, 0, 1920)  
    else:
        if id==1:
            value = (0, 0.31, 0.31, 0, 1920)
        if id==2:
            value = (600, 0.31, 0.31, 0, 1920)
        if id==3:
            value = (1200, 0.31, 0.31, 0, 1920)
        if id==4:
            value = (100, 0.21, 0.21, 0, 1920)
        if id==5:
            value = (500, 0.21, 0.21, 0, 1920)
        if id==6:
            value = (900, 0.21, 0.21, 0, 1920)  
        if id==7:
            value = (1300, 0.21, 0.21, 0, 1920) 
    return value

if __name__ == "__main__":
    setSource('1','2')
    setValue('1','2')


