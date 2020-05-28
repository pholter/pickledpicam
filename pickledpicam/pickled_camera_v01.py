import time
import io
import picamera
from PIL import Image



# Create the in-memory stream
print('Hello!')
stream = io.BytesIO()
camera = picamera.PiCamera()
#camera.start_preview()
camera.resolution = (640, 480)
time.sleep(2)
camera.capture(stream, format='jpeg',quality=10)
# "Rewind" the stream to the beginning so we can read its content
stream.seek(0)
image = Image.open(stream)
