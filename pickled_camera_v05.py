import time
import io
import picamera
from PIL import Image
from cobs import cobs
import serial
import collections
import threading
import struct

baudrate = 614400 # works
#baudrate =   921600 # works
#baudrate = 9600
baudrate = 115200
baudrate = 230400 # works
baudrate = 345600
#baudrate = 460800 # Does not work with RS485 CAN HAT sending
baudrate = 1228800
#baudrate =  2457600
ser = serial.Serial(port='/dev/ttyAMA0',baudrate = baudrate)
#ser = serial.Serial(port='/dev/ttyUSB0',baudrate = baudrate)

resolution = (640, 480)
#resolution = (1024, 780)
#resolution = (320, 200)
#resolution = (400,300)
quality = 10

# Create the in-memory stream
print('Hello! Opening camera')
camera = picamera.PiCamera()
#camera.start_preview()
camera.resolution = resolution
time.sleep(2)
picqueue = collections.deque(maxlen=10)

counter = 0

def read_pic():
    while True:
        stream = io.BytesIO()
        tc0 = time.time()
        camera.capture(stream, format='jpeg',quality=quality)
        tc1 = time.time()
        
        size_image = stream.seek(0,2)
        print('Resolution',resolution,'quality',quality,'Image size',size_image)
        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        data = stream.read(size_image)
        data_ret = {}
        data_ret['data'] = data
        data_ret['tc0'] = tc0
        data_ret['tc1'] = tc1
        picqueue.append(data_ret)

camthread = threading.Thread(target=read_pic)
print('Starting camera thread')
camthread.start()

print('Starting sending loop')
while 1:
    #image = Image.open(stream)
    if(len(picqueue) > 0):
        data_dict = picqueue.pop()
        data = data_dict['data']
        dtcap = data_dict['tc1'] - data_dict['tc0']
        data_head = b'\xCA'
        data_head += struct.pack('d',data_dict['tc0'])
        data_package = data_head + data
        data_cobs = cobs.encode(data_package)
        print('Data size',len(data),len(data_cobs))
        #ser.write(sstr.encode('utf-8'))
        data_cobs += b'\x00'
        print('Zeros',data_cobs.find(b'\x00'))
        tb = time.time()
        ser.write(data_cobs)
        ts = time.time()
        dt = ts - tb
        print('Sent data in ', dt, 'seconds','Captured in ', dtcap, 'seconds')
        time.sleep(.05)
        counter += 1



