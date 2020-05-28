import time
import io
import picamera
from PIL import Image
from cobs import cobs



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


