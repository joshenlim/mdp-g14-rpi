from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2 as cv
import numpy as np

camera = PiCamera()
camera.resolution = (640, 480)

output = PiRGBArray(camera)
camera.capture(output, 'rgb')

src = output.array
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
dst = cv.blur(src_gray, (5, 5))

cv.imshow('Input', src)
cv.imshow('Gray', src_gray)
cv.imshow('Blur', dst)
cv.waitKey(0)
