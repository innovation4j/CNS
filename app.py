from os import O_NDELAY, wait
from flask import Flask
import serial
import time
from flask import request
from flask import Response
import iot_CNS as CNS
from multiprocessing import Process
from multiprocessing import shared_memory

app = Flask(__name__)
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
#ser = serial.Serial('COM3', 115200,timeout=2)
# G0 X1800
# G0 X10 move x point
# wait 3 sec
# G0 Y90 making 
# G0 X900 go to center
# G9 X10 S3 Y90   auto process
# G28 move to home point
# G80 raspberry pi off
# G81 raspberry pi on
# G82 raspberry pi off, after 2 seconds raspberry pi on
# G83 raspberry pi off, after 3 seconds raspberry pi on

shm = shared_memory.SharedMemory(create=True, size=1)
shm.buf[0] = CNS.FLAG_WAIT

@app.route("/")
def render_script(id=None):
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=plotter,
        daemon=True
    )
    heavy_process.start()
    return Response(
        mimetype='application/json',
        status=200
    )

@app.route("/status")
def getStatus():
    # b'' --> switch off
    # else --> switch on
    # on - work   on - wait    off 
    print ("0->"+str(ser.read()))
    if(str(ser.read()) != "b''"): #on
        print ("1->"+str(ser.read()))

        print ("2->"+str(shm.buf[0]))
        if( shm.buf[0] == 0 ): #wait
            #on - wait : waiting 
            print ("2->"+str(shm.buf[0]))
            return str(CNS.FLAG_WAIT)
        elif(shm.buf[0] == 1 ): #wait
            print ("3->"+str(shm.buf[0]))
            #on - work : on working
            return str(CNS.FLAG_WORK)
    else: #off
        print ("9->"+str(ser.read()))
        return str(CNS.FLAG_SWC_OFF)


@app.route("/init")
def setInit():
    Flask.Status = "Work"
    Plotter_print = 'G28'
    ser.write(Plotter_print.encode())
    ser.write(b'\x0d\x0a')
    time.sleep(5)

    # Init positionFlask.Status
    Plotter_Init = 'G0 X900'
    print(Plotter_Init)
    print("Plotter_Init" + Plotter_Init)
    ser.write(Plotter_Init.encode())
    ser.write(b'\x0d\x0a')
    time.sleep(3)
    Flask.Status = "Wait"
    return 'init'

# G80 raspberry pi off
# G81 raspberry pi on
# G82 raspberry pi off, after 2 seconds raspberry pi on
# G83 raspberry pi off, after 3 seconds raspberry pi on
@app.route("/zero")
def setZero():
    # Init positionFlask.Status
    Plotter_Init = 'G0 X0'
    ser.write(Plotter_Init.encode())
    ser.write(b'\x0d\x0a')
    time.sleep(3)
    Flask.Status = "Wait"
    return 'zero'


@app.route("/reset")
def setReset():
    Flask.Status = "Work"
    Plotter_print = 'G83'
    print(Plotter_print)
    print("Raspberry Reset" + Plotter_print)
    ser.write(Plotter_print.encode())
    ser.write(b'\x0d\x0a')
    time.sleep(5)
    Flask.Status = "Wait"
    return 'reset'

@app.route("/rasoff")
def setRasOff():
    Flask.Status = "Work"
    Plotter_print = 'G80'
    print(Plotter_print)
    print("Raspberry Off" + Plotter_print)
    ser.write(Plotter_print.encode())
    ser.write(b'\x0d\x0a')
    time.sleep(5)
    Flask.Status = "Wait"
    return 'Raspberry Off'

@app.route("/rason")
def setRasOn():
    Flask.Status = "Work"
    Plotter_print = 'G81'
    print(Plotter_print)
    print("Raspberry On" + Plotter_print)
    ser.write(Plotter_print.encode())
    ser.write(b'\x0d\x0a')
    time.sleep(5)
    Flask.Status = "Wait"
    return 'Raspberry On'

def plotter():
    print("Flask.Status 1 " + str(Flask.Status))
    if Flask.Status == "Wait":
        Flask.Status = "Work"
        shm.buf[0] = CNS.FLAG_WORK
        print("Flask.Status 2 " + str(Flask.Status))
        wait_time = 5
        print_time = 0.3
        x_point = 30
        speed = 3000
        x_point = request.args.get('x_point')
        wait_time = request.args.get('wait_time')
        # Move X point
        Plotter_MoveX = f"G0 X{int(x_point)} F{int(speed)}"
        print("Plotter_MoveX" + Plotter_MoveX)
        print("wait_time" + wait_time)
        ser.write(Plotter_MoveX.encode())
        ser.write(b'\x0d\x0a')
        time.sleep(float(wait_time))

        # Print Plotter
        Plotter_print = 'G0 Y45'
        print("Plotter_print" + Plotter_print)
        print("print_time" + str(print_time))
        ser.write(Plotter_print.encode())
        ser.write(b'\x0d\x0a')
        time.sleep(print_time)

        # Init position
        Plotter_Init = 'G0 X900'
        print(Plotter_Init)
        print("Plotter_Init" + Plotter_Init)
        ser.write(Plotter_Init.encode())
        ser.write(b'\x0d\x0a')

        time.sleep(3)
        Flask.Status = "Wait"
        shm.buf[0] = CNS.FLAG_WAIT
        return "Plotting Complete"
    else:
        return "Plotting is not Available"

if __name__ == "__main__":
    Flask.Status = "Wait"
    setInit()
    app.run(host='0.0.0.0')
    #app.run()