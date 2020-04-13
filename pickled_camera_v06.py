import time
import io
import picamera
from PIL import Image
from cobs import cobs
import serial
import collections
import threading
import struct
import ctypes
import datetime
import glob
import os

libfullpath = '/home/pi/pickledpicam/kellerp_i2c/libread_keller_ld.so'
keller_LD = ctypes.CDLL(libfullpath)

open_keller_LD = keller_LD.open_keller_LD
close_keller_LD = keller_LD.close_keller_LD
close_keller_LD.argtypes = [ctypes.c_int]
read_keller_LD = keller_LD.read_keller_LD
read_keller_LD.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]

rx = ctypes.create_string_buffer(5)
p = ctypes.c_double()
T = ctypes.c_double()
stime = ctypes.c_double()


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
        # Read pressure information 
        read_keller_LD(sensor,rx,ctypes.byref(p),ctypes.byref(T),ctypes.byref(stime))
        tstr = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-5]
        tstr_file = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S.%f')[:-5]        
        data_str = tstr + ' p: {:3.2f}'.format(p.value) + ' T: {:3.1f}'.format(T.value)
        #print(float(p),p,T)
        print(data_str)
        camera.exif_tags['EXIF.UserComment'] = data_str.encode()
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = data_str
        camera.capture(stream, format='jpeg',quality=quality)
        tc1 = time.time()
        size_image = stream.seek(0,2)
        #print('Resolution',resolution,'quality',quality,'Image size',size_image)
        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        data = stream.read(size_image)
        data_ret = {}
        data_ret['data'] = data
        data_ret['tc0'] = tc0
        data_ret['tc1'] = tc1
        data_ret['p'] = p
        data_ret['T'] = T
        data_ret['tstr_file'] = tstr_file
        data_ret['data_str'] = data_str
        picqueue.append(data_ret)


print('Looking for files in directory')
DPATH = '/home/pi/pickledpicam/data/'
fcounter = 0
for f in glob.glob(DPATH + '*.jpg'):
    #print(f)
    try:
        fcounter_tmp = int(f.split('/')[-1].split('_')[0])
    except:
        fcounter_tmp = -1
    if(fcounter_tmp >= fcounter):
        fcounter = fcounter_tmp +1

print('Found ', fcounter, ' files in directory',DPATH)
print('Opening pressure sensor')
sensor = open_keller_LD()
camthread = threading.Thread(target=read_pic)
print('Starting camera thread')
camthread.start()

fname_log = '{:08d}'.format(fcounter) + '.log'
fname_log_full = DPATH + fname_log
flog = open(fname_log_full,'w')
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

        # Saving the file
        fname = '{:08d}'.format(fcounter) + '_' + data_dict['tstr_file'] + '.jpg'
        fname_full = DPATH + fname
        print('Saving to',fname)
        tbs = time.time()        
        f = open(fname_full,'wb')
        f.write(data)
        f.close()
        tss = time.time()
        dtsave = tss - tbs        
        fcounter += 1
        # Write the log file
        pR = data_dict['p'].value
        TR = data_dict['T'].value

        data_strR = ',p,{:3.2f}'.format(pR) + ',T,{:3.1f}'.format(TR)        
        logstr = data_dict['tstr_file'] + data_strR + ',' + fname + '\n'
        flog.write(logstr)
        flog.flush()
        print('Sent data in ', dt, 'seconds','Captured in ', dtcap, 'seconds','Saved in ',dtsave)
        
        time.sleep(.05)
        counter += 1



print('Closing pressure sensor')
close_keller_LD(sensor)
