import cv2
import numpy as np

from picamera import PiCamera
from picamera.array import PiRGBArray

# Capture frame
camera = PiCamera()
camera.vflip = True
camera.resolution = (640, 480)

output = PiRGBArray(camera)
camera.capture(output, 'rgb')
img = output.array

# Pre-process frame output
mask = np.zeros(img.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel= np.zeros((1, 65), np.float64)

rect = (50, 50, 300, 500)
cv2.grabCut(img, mask, rect, bgdModel,fgdModel, 5, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

img = img*mask2[:, :, np.newaxis]
cv2.imshow('test', img)
cv2.waitKey(0)
