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
#baudrate = 460800 # Does not work with RS485 CAN HAT sending
#baudrate = 1228800
#baudrate =  2457600
ser = serial.Serial(port='/dev/ttyAMA0',baudrate = baudrate)
#ser = serial.Serial(port='/dev/ttyUSB0',baudrate = baudrate)
counter = 0
while 1:
    sstr = 'Write counter: {:d} \n'.format(counter)
    print(sstr)
    ser.write(sstr.encode('utf-8'))
    time.sleep(1)
    counter += 1

# Create the in-memory stream
print('Hello!')
resolution = (640, 480)
quality = 5
stream = io.BytesIO()
camera = picamera.PiCamera()
#camera.start_preview()
camera.resolution = resolution
time.sleep(2)
camera.capture(stream, format='jpeg',quality=quality)
size_image = stream.seek(0,2)
print('Resolution',resolution,'quality',quality,'Image size',size_image)
# "Rewind" the stream to the beginning so we can read its content
stream.seek(0)
data = stream.read(size_image)
#image = Image.open(stream)

data_cobs = cobs.encode(data)
print(len(data),len(data_cobs))


