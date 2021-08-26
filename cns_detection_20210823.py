#%%
# import packages
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
global trackCount, equipmentId, rangeMin, rangeMax, id, settingSource, settingValue, imgLocBox, imgLocFind, imgLocBoxRef, imgLocFindRef, imgLocDetect, type_AB, startedTime, thresholdTime, printIP
global objectFr, objectTo, xMin, xMax, yMin, yMax, time_0, time_10, find, objectBox, mask, maskFlag
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
xMin=0
xMax=1920
yMin=0
yMax=1080
time_0 = None
time_10 = None
find = False
objectBox = None
mask = None
maskFlag = False
# objectFr = (x, y, w, h, size, pred)
# objectTo = (x, y, w, h, size, pred)
objectFr = (0, 0, 0, 0, 0.0, 0.0)
objectTo = (0, 0, 0, 0, 0.0, 0.0)

# Disable scientific notation
global prediction, predictionResult, data, model_AB, model

np.set_printoptions(suppress=True)
# keras Load the model
#model = tensorflow.keras.models.load_model('model_NP.h5') #model_NP
model = tensorflow.keras.models.load_model('keras_model_20210813.h5')
model_AB = tensorflow.keras.models.load_model('model_AB_20210813.h5')
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
    global equipmentId, rangeMin, rangeMax, id, settingSource, settingValue, imgLocBox, imgLocFind, imgLocBoxRef, imgLocFindRef, imgLocDetect, printIP
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

    #settingValue (x축시작좌료(mm), X축 변환값(px->mm), Y축 변환값(px->mm), x축 범위최소값, x축 범위 최대값)
    settingSource, printIP = PSET.setSource(equipmentId, id)

    settingValue = PSET.setValue(equipmentId, id)

    print(f'settingSource={settingSource}, {printIP}' )
    print(f'settingValue={settingValue}' )

    today = datetime.datetime.now().strftime("%Y%m%d")

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

    CNS.LOG(equipmentId, settingSource[0], f'{equipmentId} {settingSource[0]} Stand By')
    CNS.EXP_LOG(equipmentId, f'{equipmentId} {settingSource[0]} exp Stand By')
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
    global equipmentId, settingSource

    if type=='box_0':
        cv2.imwrite(f'{imgLocBox}{time}_00_{pred}_{size}_box.jpg', image)
    if type=='find_0':
        cv2.imwrite(f'{imgLocFind}{time}_00_{pred}_{size}.jpg', image)
    if type=='box_10':
        cv2.imwrite(f'{imgLocBox}{time}_10_{pred}_{size}_box.jpg', image)
    if type=='find_10':
        cv2.imwrite(f'{imgLocFind}{time}_10_{pred}_{size}.jpg', image)
        cv2.imwrite(f'{imgLocDetect}{time}_10_{pred}_{size}.jpg', image)
    if type=='boxRef':
        cv2.imwrite(f'{imgLocBoxRef}{time}_{pred}_{size}_box.jpg', image)
    if type=='findRef':
        cv2.imwrite(f'{imgLocFindRef}{time}_{pred}_{size}.jpg', image)
    CNS.LOG(equipmentId, settingSource[0], f'[6]	Image Store Done    {type}')

    return True
print(f'#4 Store Image  Stand By......' )

# 5. check Object Continuity, caculate velocity, printing
# (X,Y) -> (X',Y'), time, shape, size 
# objectFr = (x, y, w, h, size, pred)
# objectTo = (x, y, w, h, size, pred)
def objectProcessing(objectFr, objectTo, time_0, time_10):
    isContinue = False
    CNS.LOG(equipmentId, settingSource[0], f'[3]	Detected ')

    if ( objectFr[0]-200 < objectTo[0] < objectFr[0]+200 ):
        if( objectFr[1]+200 < objectTo[1] ):
            if( 0.6 < objectFr[4]/objectTo[4] < 1.4 ):
                #OK
                isContinue = True

    if (isContinue):
        CNS.LOG(equipmentId, settingSource[0], f'[4]	Continued ')
        # distance
        movePx = objectTo[1] - objectFr[1]
        moveMM = round(movePx*settingValue[1])

        # velocity
        time_diff = time_10 - time_0

        diff_sec = int(str(time_diff)[5:7])*1000 #sec
        time_diff2 = diff_sec+int(str(time_diff)[8:11]) #sec+microsec
        currentV = round( moveMM / int(time_diff2), 2 )

        CNS.LOG(equipmentId, settingSource[0], f'[4-1]	Velocity : {currentV} ')
        # time(ms) = distance to pan (1150mm)+ Y axis (mm covnert value) / velocity
        # 1150 + 1080 - 800 
        printLead = (1080-objectTo[1])*settingValue[1] + 1000
        printTime = round( printLead / currentV / 1000, 1)  #초로 변환
        printPositionVal = settingValue[0] + round((objectTo[0])*settingValue[1])# objectX + camera position value 

        CNS.LOG(equipmentId, settingSource[0], f'[4-2]	PrintInfo	printTime	{printTime}	Position	{printPositionVal} ')

        if(printTime > 2 and printTime < 7):
            printInk(printPositionVal, printTime)
            CNS.LOG(equipmentId, settingSource[0], f'[4-3]	Print Called')
        else:
            CNS.LOG(equipmentId, settingSource[0], f'[4-E1]	Print Time Out Of Range')
            return False

    else:
        CNS.LOG(equipmentId, settingSource[0], f'[4-E2]	Not Continued ')
        return False
    return True
print(f'#5 Object Check Stand By......' )

# 6. print
def printInk(axis_x, float_sec):
    # Plotter_Xposition = int(camPosition) + int(objectX)
    CNS.LOG(equipmentId, settingSource[0], f'[5] Printing start')
    try:
        Plotter_Status = requests.get(f"{printIP}/status").text
        if Plotter_Status == "0":
            print_order = f"{printIP}/?x_point={int(axis_x)}&wait_time={float_sec}"
            try:
                res = requests.get(print_order)
                CNS.LOG(equipmentId, settingSource[0], f'[5-1]	Printing Done')
                return True
            except:
                try:
                    print_order = f"{printIP}/init"
                except:
                    CNS.LOG(equipmentId, settingSource[0], f'[5-E1]	Plotting is not Available')
                    return False
                return False
        else:
            CNS.LOG(equipmentId, settingSource[0], f'[5-E2]	Plotter is Working')
            return False
        return True
    except:
        CNS.LOG(equipmentId, settingSource[0], f'[5-E3]	Plotter not response')
        return False
print(f'#6 Print Stand By......' )


# 7. reset
def resetStatus():
    global trackCount, time_0, time_10, objectFr, objectTo, xMin, xMax, yMin, yMax, find, objectBox, type_AB, startedTime, thresholdTime, maskFlag
    trackCount = 0
    time_0=None
    time_10=None
    objectFr = (0, 0, 0, 0, 0.0, 0.0)
    objectTo = (0, 0, 0, 0, 0.0, 0.0)
    xMin=0
    xMax=1920
    yMin=0
    yMax=1080
    find = False
    objectBox=None
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
        # ASIS        
        # points = int(height/2), int(height/2+224), int(width/2), int(width/2+224)
        # roi = frame[points[0]:points[1], points[2]:points[3], :]
        # plt.imshow(roi)
        # result = checkTypeAB(roi)

        

        width_start = np.int(width*0/4)
        width_end = np.int(width*1/4)
        roi = frame[:, width_start:width_end,:] # 세로 전부 (:), 채널 전부 (:)
        #roi = frame.fromarray(roi)
        result = checkTypeAB(roi)

        if (round(float(result[0][0]),3) > 0.50):
            type_AB = "A"
            startedTime = datetime.datetime.now()
            print(f'Type A : {round(float(result[0][0])*100,3)}% {type_AB}' )
            print(f'Type B : {round(float(result[0][1])*100,3)}%' )
            print(f'startedTime......{startedTime}' )        
        elif (round(float(result[0][0]),3) <= 0.50):
            type_AB = "B"
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

            if( objectFr[5] > 0.95 ):
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

                time_0 = datetime.datetime.now()
                storeImage(objectBox, 'box_0', size, objectFr[5], time_0.strftime("%Y%m%d%H%M%S"))
                objectBox = None
                find = True
                xMin = x-200
                xMax = x+200
                yMin = y
                trackCount = 0

                CNS.LOG(equipmentId, settingSource[0], f'[1]	FirstFind	pred	{objectFr[5]}	xMin~xMax	({xMin}~{xMax})	(x,y,w,h)	{x, y, w, h}	objectFr	{objectFr}	time_00	{time_0}')

                #find image 저장 
                cv2.rectangle(frame, (angleX1,angleY1), (angleX2, angleY2), (0, 0, 255), 1)
                cv2.putText(frame, f"x:{x},:y {y}, size:{size}", (angleX1, angleY2),cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255])            
                cv2.putText(frame, f"prediction :{objectFr[5]}", (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255])            
                storeImage(frame, 'find_0', size, objectFr[5], time_0.strftime("%Y%m%d%H%M%S"))
            else:
                trackCount = 0

        if(find and trackCount in (5,10,15) ):
            objectTo = (0, 0, 0, 0, 0.0, 0.0)
            time_10 = datetime.datetime.now()    
            for detected in contours:
                size = cv2.contourArea(detected)
                x, y, w, h = cv2.boundingRect(detected)
                if (rangeMin<size<rangeMax and xMin < x < xMax and y > yMin):
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
                    
                    box = frame[boxY:boxY+boxH,boxX:boxX+boxW]


                    pred = checkObject(w, h, box)
                    if( objectTo[5] == 0.0):
                        objectTo = (x, y, w, h, size, pred)
                        objectBox = box
                    else:
                        if( objectTo[5] < pred ):
                            objectTo = (x, y, w, h, size, pred)
                            objectBox = box

            if( objectTo[5] > 0.95 ):

                x, y, w, h, size = objectTo[0], objectTo[1], objectTo[2], objectTo[3], objectTo[4]            
                CNS.LOG(equipmentId, settingSource[0], f'[2]	SecondFind	pred	{objectTo[5]}	xMin~xMax	({xMin}~{xMax})	(x,y,w,h)	{x, y, w, h}	objectTo	{objectTo}	time_10	{time_10}')            

                #2021-03-17 rectangle size modify
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

                if( objectProcessing(objectFr, objectTo, time_0, time_10) ):
                    storeImage(objectBox, 'box_10', size, objectTo[5], time_10.strftime("%Y%m%d%H%M%S"))
                    cv2.rectangle(frame, (angleX1,angleY1), (angleX2, angleY2), (0, 0, 225), 1)
                    cv2.putText(frame, f"x:{x},:y {y}, size:{size}", (int(x - 100), int(y + 150)),cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255])       
                    cv2.putText(frame, f"prediction :{objectTo[5]}", (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255])    
                    cv2.imshow('Input', frame)
                    storeImage(frame, 'find_10', size, objectTo[5], time_10.strftime("%Y%m%d%H%M%S"))
                    CNS.LOG(equipmentId, settingSource[0], f'[10]	Detect process Success')                    
                    #export log
                    CNS.EXP_LOG(equipmentId, f'{equipmentId}|{settingSource[0]}|{time_10.strftime("%Y%m%d")}|{time_10.strftime("%H%M%S")}|{objectTo[5]}|{size}|{x},{y}|{time_10.strftime("%Y%m%d%H%M%S")}_10_{objectTo[5]}_{size}.jpg')
                    time.sleep(3)
                    CNS.LOG(equipmentId, settingSource[0], f'[11]	Sleep Done')
                    find = False


            if ( 0.70 < objectTo[5] <= 0.95):
                CNS.LOG(equipmentId, settingSource[0], f'[3]	Reference	pred	{objectTo[5]}	xMin~xMax	({xMin}~{xMax})	(x,y,w,h)	{x, y, w, h}	objectTo	{objectTo}')
                storeImage(objectBox, 'boxRef', size, objectTo[5], time_10.strftime("%Y%m%d%H%M%S"))
                cv2.rectangle(frame, (angleX1,angleY1), (angleX2, angleY2), (0, 0, 225), 1)
                cv2.putText(frame, f"x:{x},:y {y}, size:{size}", (angleX1, angleY2),cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255])            
                cv2.putText(frame, f"prediction :{objectTo[5]}", (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255])            
                storeImage(frame, 'findRef', size, objectTo[5], time_10.strftime("%Y%m%d%H%M%S"))
                CNS.LOG(equipmentId, settingSource[0], f'[12]	Reference Done')
                find = False
    trackCount = trackCount + 1
    if(trackCount > 15 ):
        resetStatus()    

    k = cv2.waitKey(1)
    if k == 27:  # Escape
        break
    success, frame = cap.read()


cap.release()
cv2.destroyAllWindows()






