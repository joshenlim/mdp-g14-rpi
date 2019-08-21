from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.vflip = True
camera.start_preview()
sleep(10)
camera.stop_preview()
