#%%
# import packages
# 
# -----------------------------------------------------------------------
from matplotlib import image
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import cv2
import datetime
import sys
import time
import requests
import asyncio
import glob
import os
import iot_CNS as CNS
import preSetting as PSET
# -----------------------------------------------------------------------

# Boolean

# Variable
dim = (224, 224)
global trackCount, equipmentId, rangeMin, rangeMax, id, settingSource, settingValue, imgLocBox, imgLocFind, imgLocBoxRef, imgLocFindRef, imgLocDetect, type_AB, startedTime, thresholdTime, printIP, today
global objectFr, time_0, objectBox, mask, maskFlag, find, printYn, switchOnOff
trackCount = 0
equipmentId = None
rangeMin = 50
rangeMax = 2000
id = 14
settingSource = ("", "")
#settingValue (x축 시작위치, X축 변환값, Y축 변환값, x축 범위최소값, x축 범위 최대값)
settingValue = (0, 0, 0, 0, 0)
imgLocBox = ""
imgLocFind = ""
imgLocBoxRef = ""
imgLocFindRef = ""
imgLocDetect = ""
type_AB = ""
startedTime = None
thresholdTime = None
printIP = ""
today = ""
time_0 = None
objectBox = None
mask = None
maskFlag = False
find = False
printYn = ""
switchOnOff = ""
# objectFr = (x, y, w, h, size, pred)
# objectTo = (x, y, w, h, size, pred)
objectFr = (0, 0, 0, 0, 0.0, 0.0)
#objectTo = (0, 0, 0, 0, 0.0, 0.0)

# Disable scientific notation
global prediction, predictionResult, data, model_AB, model

np.set_printoptions(suppress=True)
# keras Load the model
#model = tensorflow.keras.models.load_model('model_NP.h5') #model_NP
model = tensorflow.keras.models.load_model('keras_model_20210824.h5')
model_AB = tensorflow.keras.models.load_model('model_AB_20210904.h5')
#model_AB = tensorflow.keras.models.load_model('model_AB.h5')
# Create the array of the right shape
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
# set parameters for BackgroundSubtractorKNN
prediction = None #model.prediction(data)
predictionResult = 0.0
bg_subtractor = cv2.createBackgroundSubtractorKNN(detectShadows=True)
history_length = 20
bg_subtractor.setHistory(history_length)
# remove image sensor noise
erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))


######################## function define ########################
# 1. input Validation
def validationInput(inputArr):
    # settingValue = (cam_name, url, xVal, convert_X, Convert_Y, xRangeMin, xRangeMax)
    global equipmentId, rangeMin, rangeMax, id, settingSource, settingValue, imgLocBox, imgLocFind, imgLocBoxRef, imgLocFindRef, imgLocDetect, printIP, today
    if len(inputArr) == 5:
        equipmentId = inputArr[1]
        rangeMin = int(inputArr[2])
        rangeMax = int(inputArr[3])
        id = int(inputArr[4])
    else:
        rangeMin = 50
        rangeMax = 2000
        id = 0

    print(f'equipmentId={equipmentId}, rangeMin~rangeMax:{rangeMin}~{rangeMax}, id={id}' )

    settingSource, printIP = PSET.setSource(equipmentId, id)
    settingValue = PSET.setValue(equipmentId, id)

    today = datetime.datetime.now().strftime("%Y%m%d")
    
    mkdir(today)

    return True
print(f'#1 InputValidation Stand By......' )



# 2.1 Source_type check
def checkTypeAB(box):
    global model_AB

    # resize the image to a 224x224
    image_array = cv2.resize(box, dsize=dim, interpolation=cv2.INTER_CUBIC)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array
    # run the inference
    prediction = model_AB.predict(data)
    # CN S.LOG(camPosition, prediction)
    # Generate arg maxes for predictions
    np.argmax(prediction, axis=1)
    return prediction

# 2. image Prediction
def predict(box):
    global data, model, predictionResult
    # resize the image to a 224x224
    image_array = cv2.resize(box, dsize=dim, interpolation=cv2.INTER_CUBIC)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array
    # run the inference
    prediction = model.predict(data)
    # CN S.LOG(camPosition, prediction)
    # Generate arg maxes for predictions
    np.argmax(prediction, axis=1)
    predictionResult = round(float(prediction[0][0]),3)
    return predictionResult
print(f'#2 Predict Stand By......' )

# 3. check Object
def checkObject(w, h, box):

    resized_image = cv2.resize(box, dim, interpolation=cv2.INTER_AREA)

    predictionResult = predict(resized_image)

    if(  0.25 < round(w/h,2) < 4):
        return predictionResult
    else: return 0


print(f'#3 Object Check Stand By......' )

# 4. image Store
def storeImage(image, type, size, pred, time):
    global equipmentId, settingSource, today

    if today != datetime.datetime.now().strftime("%Y%m%d") : 
        today = datetime.datetime.now().strftime("%Y%m%d")
        mkdir(today)

    if type=='box_0':
        cv2.imwrite(f'{imgLocBox}{time}_00_{pred}_{size}_box.jpg', image)
    if type=='find_0':
        cv2.imwrite(f'{imgLocFind}{time}_00_{pred}_{size}.jpg', image)
        cv2.imwrite(f'{imgLocDetect}{time}_00_{pred}_{size}.jpg', image)
    if type=='boxRef':
        cv2.imwrite(f'{imgLocBoxRef}{time}_{pred}_{size}_box.jpg', image)
    if type=='findRef':
        cv2.imwrite(f'{imgLocFindRef}{time}_{pred}_{size}.jpg', image)
    CNS.LOG(equipmentId, settingSource[0], f'[6]	Image Store Done    {type}')

    return True
print(f'#4 Store Image  Stand By......' )


def objectProcessingSimple(objectFr):
    global printYn
    printYn = ""
    isContinue = False
    CNS.LOG(equipmentId, settingSource[0], f'[4]	Continued ')
    # distance

    printLead = (1080-objectFr[1])*settingValue[1] + 700
    printTime = round( ( printLead / 0.333 ) / 1000, 1)  #초로 변환

    if equipmentId == "mb3":
        if ( settingSource[0] in ("t1","t2","t3") ):
            printPositionVal = settingValue[0] + round((objectFr[0])*settingValue[1])# objectX + camera position value 
        elif ( settingSource[0] in ("b1","b2","b3","b4") ):
            printPositionVal = settingValue[0] + round((1920-objectFr[0])*settingValue[1])
            #b1의 경우 0 부터 시작하고 450mm 레인지임 이고 X축이 0에서 얼마나 떨어져 있는지 설정해야 함
            #X가 500px일 경우 1920에서 500을뺀 나머지 1420을 mm로 환산해서 셋팅해야함
            #X가 500px일 경우 1420*0.21 = 298mm , 298mm+0mm 298mm이므로 플로터는 298mm로 이동해야 함.
    elif equipmentId in ( "mb4", "mb5","mb5"):
        if ( settingSource[0] in ("t1","t2","t3") ):
            printPositionVal = settingValue[0] + round((objectFr[0])*settingValue[1])# objectX + camera position value 
        elif ( settingSource[0] in ("b1","b2","b3","b4") ):
            #b1의 경우 100 부터 시작하고 400mm 레인지임 이고 X축이 100에서 얼마나 떨어져 있는지 설정해야 함
            #X가 500px일 경우 1920에서 500을뺀 나머지 1420을 mm로 환산해서 100에 더해줘야 함.
            #X가 500px일 경우 1420*0.21 = 298mm , 100mm+298mm 398mm이므로 플로터는 398mm로 이동해야 함.
            printPositionVal = settingValue[0] + round((1920-objectFr[0])*settingValue[1])
    else :
        return False

    CNS.LOG(equipmentId, settingSource[0], f'[4-2]	PrintInfo	printTime	{printTime}	Position	{printPositionVal} ')

    if(printTime > 2 and printTime < 7 and objectFr[5] >= 0.99):
        printYn = printInk(printPositionVal, printTime)
        CNS.LOG(equipmentId, settingSource[0], f'[4-3]	Print Called printYn{printYn}')
        return True
    else:
        CNS.LOG(equipmentId, settingSource[0], f'[4-E1]	Print Time Out Of Range of under 99%')
        return False

    return True

# 6. print
def printInk(axis_x, float_sec):
    global switchOnOff
    switchOnOff = ""
    # Plotter_Xposition = int(camPosition) + int(objectX)
    CNS.LOG(equipmentId, settingSource[0], f'[5] Printing start')
    try:
        Plotter_Status = requests.get(f"{printIP}/status").text

        if Plotter_Status == 0: #waiting
            switchOnOff = "on"
            print_order = f"{printIP}/?x_point={int(axis_x)}&wait_time={float_sec}"
            try:
                res = requests.get(print_order)
                CNS.LOG(equipmentId, settingSource[0], f'[5-1]	Printing Done')
                return True
            except:
                try:
                    print_order = f"{printIP}/init"
                except:
                    CNS.LOG(equipmentId, settingSource[0], f'[5-E1]	Plotter_Status : {Plotter_Status} Plotting is not Available')
                    return False
                return False
        elif Plotter_Status == 1: #working
            switchOnOff = "on"
            CNS.LOG(equipmentId, settingSource[0], f'[5-E2]	Plotter_Status : {Plotter_Status} Plotter is Working')
            return False
        elif Plotter_Status == 9: #off
            switchOnOff = "of"
            CNS.LOG(equipmentId, settingSource[0], f'[5-E2]	Plotter_Status : {Plotter_Status} Plotter is Working')
            return False
        else:
            return True
    except:
        CNS.LOG(equipmentId, settingSource[0], f'[5-E3]	Plotter not response')
        return False
print(f'#6 Print Stand By......' )


# 7. reset
def resetStatus():
    global time_0, objectFr, objectBox, type_AB, startedTime, thresholdTime, maskFlag, find
    time_0=None
    objectFr = (0, 0, 0, 0, 0.0, 0.0)
    objectBox=None
    find = False
    trackCount = 0
    #CN S.LOG(settingSource[0], f'Reset' )

    if( type_AB != "" and startedTime != None):
        now = datetime.datetime.now()
        if ((now - startedTime).seconds/60 > 1 ):
            print(f'startedTime : {startedTime}    now : {now} diff : {(now - startedTime).seconds}')
            type_AB = ""
            startedTime = None

    if( maskFlag == True and thresholdTime != None ):
        now = datetime.datetime.now()
        if ((now - thresholdTime).seconds/60 > 1 ):
            print(f'thresholdTime : {thresholdTime}    now : {now} diff : {(now - thresholdTime).seconds}')
            maskFlag = False

    return True
print(f'#7 Status reset Stand By......' )



# 8. Threshold
def threshold(frame):
    global mask, thresholdTime, maskFlag
    thresholdTime = datetime.datetime.now()
    # 1.threshold  
    # if pixel is > 80, pixel value = 255 else pixel value 0
    print(f'frame {frame.shape}')
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print(f'grayFrame {grayFrame.shape}')
    #plt.imshow(grayFrame, cmap='gray')
    (T, threshold) = cv2.threshold(grayFrame, 80, 255, cv2.THRESH_BINARY)
    thresh_with_blur = cv2.medianBlur(threshold, 15, 0)
    #plt.imshow(thresh_with_blur, cmap='gray')

    # extract forground
    mask = cv2.bitwise_and(grayFrame, grayFrame, mask=thresh_with_blur)
    maskFlag = True
    #plt.imshow(mask, cmap='gray')

    return True
print(f'#8. Threshold Stand By......' )

def mkdir(today):
    global equipmentId, settingSource, imgLocBox, imgLocFind, imgLocBoxRef, imgLocFindRef, imgLocDetect 

    if ( settingSource[0] in ("t1","t2","t3") ):
        imgLocBox    = f"image_storage/{equipmentId}_top/{today}/{settingSource[0]}/box/"
        imgLocFind   = f"image_storage/{equipmentId}_top/{today}/{settingSource[0]}/find/"
        imgLocBoxRef = f"image_storage/{equipmentId}_top/{today}/{settingSource[0]}_ref/box/"
        imgLocFindRef= f"image_storage/{equipmentId}_top/{today}/{settingSource[0]}_ref/find/"
        imgLocDetect = f"image_storage/{equipmentId}_top/{today}/detection/"
    elif ( settingSource[0] in ("b1","b2","b3","b4") ):
        imgLocBox    = f"image_storage/{equipmentId}_btm/{today}/{settingSource[0]}/box/"
        imgLocFind   = f"image_storage/{equipmentId}_btm/{today}/{settingSource[0]}/find/"
        imgLocBoxRef = f"image_storage/{equipmentId}_btm/{today}/{settingSource[0]}_ref/box/"
        imgLocFindRef= f"image_storage/{equipmentId}_btm/{today}/{settingSource[0]}_ref/find/"
        imgLocDetect = f"image_storage/{equipmentId}_btm/{today}/detection/"
    else:
        imgLocBox    = f"image_storage/{equipmentId}/{today}/{settingSource[0]}/box/"
        imgLocFind   = f"image_storage/{equipmentId}/{today}/{settingSource[0]}/find/"
        imgLocBoxRef = f"image_storage/{equipmentId}/{today}/{settingSource[0]}_ref/box/"
        imgLocFindRef= f"image_storage/{equipmentId}/{today}/{settingSource[0]}_ref/find/"
        imgLocDetect = f"image_storage/{equipmentId}/{today}/detection/"
        


    if not os.path.exists(imgLocBox):
        os.makedirs(imgLocBox)
    if not os.path.exists(imgLocFind):
        os.makedirs(imgLocFind)
    if not os.path.exists(imgLocBoxRef):
        os.makedirs(imgLocBoxRef)
    if not os.path.exists(imgLocFindRef):
        os.makedirs(imgLocFindRef)
    if not os.path.exists(imgLocDetect):
        os.makedirs(imgLocDetect)
    return True

print(f'#All Stand By..................................................' )

######################## main process start #############################
validationInput(sys.argv)

cap = cv2.VideoCapture(settingSource[1])
#cap = cv2.VideoCapture(0)

success, frame = cap.read()


# frame demension
fshape = frame.shape 
fheight = fshape[0]
fwidth = fshape[1]
fps = int(cap.get(cv2.CAP_PROP_FPS))
print(f'Width:{fwidth}, Height:{fheight}, FPS:{fps}' )

# loop
while success:

    if(maskFlag==False):
        threshold(frame)
        print(f'#threshold Stand By..................................................' )

    frame = cv2.bitwise_and(frame, frame, mask=mask)
    # check Type A or B
    if (type_AB == ""):


        height, width, channels = frame.shape
        
        

        # right 25%
        if ( settingSource[0] in ("t1","b4") ):
            print(f'Get right 25%' )
            points = int(height/2), int(height/2+224), int(width-224), int(width)
        # left 25%
        elif ( settingSource[0] in ("t2", "t3", "b1") ):
            print(f'Get left 25%' )
            points = int(height/2), int(height/2+224), int(0), int(224)            
        elif ( settingSource[0] in ("b2", "b3") ):
            print(f'Get center 25%' )
            points = int(height/2), int(height/2+224), int(width/2), int(width/2+224)
        else :
            print(f'Get center 25%' )
            points = int(height/2), int(height/2+224), int(width/2), int(width/2+224)


        roi = frame[points[0]:points[1], points[2]:points[3], :]
        plt.imshow(roi)

        roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)        
        result = checkTypeAB(roi)


        if (round(float(result[0][0]),3) > 0.50):
            type_AB = "A"
            startedTime = datetime.datetime.now()
            print(f'Type A : {round(float(result[0][0])*100,3)}% {type_AB}' )
            print(f'Type B : {round(float(result[0][1])*100,3)}%' )
            print(f'startedTime......{startedTime}' )        
        elif (round(float(result[0][0]),3) <= 0.50):
            type_AB = "B"
            #type_AB = "A"
            startedTime = datetime.datetime.now()
            print(f'Type A : {round(float(result[0][0])*100,3)}%' )
            print(f'Type B : {round(float(result[0][1])*100,3)}% {type_AB}' )
            print(f'startedTime......{startedTime}' )        
        CNS.LOG(equipmentId, settingSource[0], f'{startedTime} , Type_AB : {round(float(result[0][0]),3)}% {type_AB}')    

    if( type_AB == "A"):
        fg_mask = bg_subtractor.apply(frame)
        ret, thresh = cv2.threshold(fg_mask, 100, 255, cv2.THRESH_BINARY)

        # Removing image sensor noise
        cv2.erode(thresh, erode_kernel, thresh, iterations=2)
        cv2.dilate(thresh, dilate_kernel, thresh, iterations=2)
        contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #최초발견
        if(find == False):
            objectFr = (0, 0, 0, 0, 0.0, 0.0)
            #가장 점수가 높은 object 추출
            
            for detected in contours:
                size = cv2.contourArea(detected)
                if (rangeMin<size<rangeMax):
                    x, y, w, h = cv2.boundingRect(detected)

                    boxY = y - h
                    if(boxY < 0):
                        boxY = 0

                    boxX = x - w
                    if(boxX < 0):
                        boxX = 0
                        
                    boxW = w*3
                    if(boxX+boxW > 1920):
                        boxW = 1920 - boxX
                    
                    boxH = h*3
                    if(boxY+boxH > 1080):
                        boxH = 1080 - boxY
                    
                    #프레임에서 박스 추출
                    box = frame[boxY:boxY+boxH,boxX:boxX+boxW]
                    pred = checkObject(w, h, box)
                    if( objectFr[5] == 0.0):
                        objectFr = (x, y, w, h, size, pred)  
                        objectBox = box
                    else:
                        if( objectFr[5] < pred ):
                            objectFr = (x, y, w, h, size, pred)
                            objectBox = box
            
            time_0 = datetime.datetime.now()

            if( objectFr[5] > 0.90 ):
                find = True
                trackCount = 0
                x, y, w, h, size = objectFr[0], objectFr[1], objectFr[2], objectFr[3], objectFr[4]

                angleX1 = x - w*3
                angleX2 = x + (w*4)
                angleY1 = y - h*3
                angleY2 = y + (h*4)

                if(angleX1 < 0):
                    angleX1 = 0
                
                if(angleY1 < 0):
                    angleY1 = 0

                    
                if(angleX2 > 1920):
                    angleX2 = 1920
                
                if(angleY2 > 1080):
                    angleY2 = 1080  
                    
                if( objectProcessingSimple(objectFr)):                
                    storeImage(objectBox, 'box_0', size, objectFr[5], time_0.strftime("%Y%m%d%H%M%S"))
                    CNS.LOG(equipmentId, settingSource[0], f'[1]	FirstFind	pred	{objectFr[5]}	(x,y,w,h)	{x, y, w, h}	objectFr	{objectFr}	time_00	{time_0}')

                    #find image 저장 
                    cv2.rectangle(frame, (angleX1,angleY1), (angleX2, angleY2), (0, 0, 255), 1)
                    cv2.putText(frame, f"x:{x},:y {y}, size:{size}", (angleX1, angleY2),cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255])            
                    cv2.putText(frame, f"prediction :{objectFr[5]}", (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255])            
                    storeImage(frame, 'find_0', size, objectFr[5], time_0.strftime("%Y%m%d%H%M%S"))
                    #export log
                    CNS.EXP_LOG(equipmentId, settingSource[0], f'{equipmentId}|{settingSource[0]}|{time_0.strftime("%Y%m%d")}|{time_0.strftime("%H%M%S")}|{objectFr[5]}|{size}|{x},{y}|{time_0.strftime("%Y%m%d%H%M%S")}_00_{objectFr[5]}_{size}.jpg|{printYn}|{switchOnOff}')
                    CNS.LOG(equipmentId, settingSource[0], f'[10]	Detect process Success')                                        
                    #cv2.imshow('Input', frame)
                    time.sleep(3)
                    CNS.LOG(equipmentId, settingSource[0], f'[11]	Sleep Done')
                else:
                    CNS.LOG(equipmentId, settingSource[0], f'[99]	PrintError')
            
            if ( 0.70 < objectFr[5] <= 0.90):
                find = True
                trackCount = 0
                x, y, w, h, size = objectFr[0], objectFr[1], objectFr[2], objectFr[3], objectFr[4]

                angleX1 = x - w*3
                angleX2 = x + (w*4)
                angleY1 = y - h*3
                angleY2 = y + (h*4)

                if(angleX1 < 0):
                    angleX1 = 0
                
                if(angleY1 < 0):
                    angleY1 = 0

                    
                if(angleX2 > 1920):
                    angleX2 = 1920
                
                if(angleY2 > 1080):
                    angleY2 = 1080              

                CNS.LOG(equipmentId, settingSource[0], f'[3]	Reference	pred	{objectFr[5]}	(x,y,w,h)	{x, y, w, h}	objectFr	{objectFr}')
                storeImage(objectBox, 'boxRef', size, objectFr[5], time_0.strftime("%Y%m%d%H%M%S"))
                cv2.rectangle(frame, (angleX1,angleY1), (angleX2, angleY2), (0, 0, 225), 1)
                cv2.putText(frame, f"x:{x},:y {y}, size:{size}", (angleX1, angleY2),cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255])            
                cv2.putText(frame, f"prediction :{objectFr[5]}", (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255])            
                storeImage(frame, 'findRef', size, objectFr[5], time_0.strftime("%Y%m%d%H%M%S"))
                CNS.LOG(equipmentId, settingSource[0], f'[12]	Reference Done')

    trackCount = trackCount + 1
    if(trackCount > 20 ):
        resetStatus()    

    k = cv2.waitKey(1)
    if k == 27:  # Escape
        break
    success, frame = cap.read()


cap.release()
cv2.destroyAllWindows()






