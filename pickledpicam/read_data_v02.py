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
baudrate = 1228800
#baudrate =  2457600
#ser = serial.Serial(port='/dev/ttyAMA0',baudrate = baudrate)
ser = serial.Serial(port='/dev/ttyUSB0',baudrate = baudrate)
dread = b''
counter = 0
while 1:
    n = ser.inWaiting()
    #print(n)
    if(n > 0):
        print(counter)
        dread += ser.read(n)
        print('Zeros',dread.rfind(b'\x00'))
        ind_zero = dread.rfind(b'\x00')
        if(ind_zero > 0):
            ind_zero0 = dread[:ind_zero].rfind(b'\x00')
            #print()
            if(ind_zero0 >= 0):
                print('Found frame',ind_zero0,ind_zero)
                cobs_data = dread[ind_zero0+1:ind_zero]
                data = cobs.decode(cobs_data)
                print('fsd',dread[ind_zero:])
                dread = dread[ind_zero:]
                if(len(data) > 10):
                    print('Opening image')
                    stream = io.BytesIO()
                    stream.write(data)
                    stream.seek(0)
                    try:
                        image = Image.open(stream)
                        image.show()
                    except Exception as e:
                        print(str(e))
                        
    time.sleep(.01)
    counter += 1
