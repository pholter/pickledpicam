import time
import io
import picamera
from PIL import Image
from cobs import cobs
import serial


baudrate = 614400 # works
#baudrate =   921600 # works
#baudrate = 9600
baudrate = 115200
baudrate = 230400 # works
baudrate = 345600
baudrate = 460800 # Does not work with RS485 CAN HAT sending
baudrate = 1228800
#baudrate =  2457600
ser_out = serial.Serial(port='/dev/ttyAMA0',baudrate = baudrate)
ser_in = serial.Serial(port='/dev/ttyUSB0',baudrate = baudrate)
counter = 0
while 1:
    counter += 1
    print('Baudrate',baudrate)
    sstr = 'Write counter: {:d} \n'.format(counter)
    sstr += sstr
    sstr += sstr
    sstr += sstr
    sstr += sstr    
    sout = sstr.encode('utf-8')    
    print('Write',len(sout))
    t0 = time.time()
    ser_out.write(sout)
    t1 = time.time()
    dt = t1-t0
    bps = len(sout)/dt * 8
    print('Wrote',sout,'dt',dt,'bits/s',bps)    
    time.sleep(.1)
    n = ser_in.inWaiting()
    if(n > 0):
        print('Read',n)
        dread = ser_in.read(n)
        print('Read',dread)

    print('')
    time.sleep(1)        




