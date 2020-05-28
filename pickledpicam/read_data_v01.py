import time
import io
import picamera
from PIL import Image
from cobs import cobs
import serial

baudrate = 614400 # works
#baudrate =   921600 # works
baudrate = 230400 # works
baudrate = 345600
#baudrate = 9600
#baudrate = 1228800
#baudrate =  2457600
#ser = serial.Serial(port='/dev/ttyAMA0',baudrate = baudrate)
ser = serial.Serial(port='/dev/ttyUSB0',baudrate = baudrate)
while 1:
    n = ser.inWaiting()
    print(n)
    if(n > 0):
        dread = ser.read(n)
        print(dread)
    time.sleep(.5)
