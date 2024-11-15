# python /home/evgenvt/Documents/projectPG/rpi-bluetooth-arduino-master/pythonClient/client.py
from flask import Flask
from threading import Thread
from flask import render_template
import time
import serial
import datetime

app = Flask(__name__)


def logData(ls):
    with open("/home/evgenvt/Documents/projectPG/rpi-bluetooth-arduino-master/pythonClient/log.txt", "a") as file:
        file.write(f"{datetime.datetime.now()}: ")
        file.write(f"{ls}\n")
        
ser = serial.Serial(
    port='/dev/rfcomm0',
    baudrate= 115200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

def readTemp():
    ser.isOpen()
    global recv1;
    global recv2;
    global recv3;
    dt = ["", "", ""]
    while 1 :
        tic = time.time()
        while time.time() - tic < 15 and ser.inWaiting() == 0: 
            time.sleep(1)
        
        for i in range(3):
            if ser.inWaiting() > 0:
                recv1 = ser.readline().rstrip().decode()
                logData(recv1)
                dt[i] = recv1
        recv1 = dt[0]
        recv2 = dt[1]
        recv3 = dt[2]
        time.sleep(4)


@app.route('/')
def index():
    return render_template("hello.html", 
                            data1 = recv1,
                            data2 = recv2, 
                            data3 = recv3)
                            
t = Thread(target = readTemp)
t.start()

if __name__ == '__main__':
    app.run()
