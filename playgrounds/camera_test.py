from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep

camera = PiCamera()
camera.resolution = (540, 480)
camera.framerate = 30
camera.vflip = False
camera.hflip = False

# camera.start_preview()
# sleep(10)
# camera.stop_preview()
