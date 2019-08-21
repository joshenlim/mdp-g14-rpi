from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2 as cv
import numpy as np
import time
import os

from src.config import CAMERA_RES_WIDTH
from src.config import CAMERA_RES_HEIGHT
from src.config import CAMERA_FRAMERATE
from src.config import SYMBOL_TYPES
from src.config import IMG_DIR
from src.detector.utils import flatten_image

'''
Standalone script to extract threshold images of each symbol
to train the image classifier for symbol recognition.
Due to the black backgrounds of the symbol cards, we'll first
detect where the symbol card is first, and warp its perspective
to create a flat top-down view of the symbol card to ensure
consistency for each symbol when generating threshold image.
Thereafter the top-down view will be used to generate the threshold
image and saved into a folder in the root directory.

Each image will follow the same pre-processing of firstly converting
to grayscale, then applying Gaussian Blur prior to generating the
treshold images.
'''

# For Blue, White, Green, Yellow, 100 seems good
# For Red, threshold has to be brought down to 30
threshold = 100

camera = PiCamera()
camera.resolution = (CAMERA_RES_WIDTH, CAMERA_RES_HEIGHT)
camera.framerate = CAMERA_FRAMERATE
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(CAMERA_RES_WIDTH, CAMERA_RES_HEIGHT))

# Allow time for camera to initialize
time.sleep(1)

for name in SYMBOL_TYPES:
    filename = name + '.jpg'

    print('Press "p" to take a picture of ' + filename)

    rawCapture.truncate(0)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv.imshow("Frame", image)

        key = cv.waitKey(1) & 0xFF
        if key == ord("p"):
            break
        rawCapture.truncate(0)

    # Begin processing snapped image
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv.threshold(blur, 100, 255, cv.THRESH_BINARY)

    _, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        print('Error: No Contours Found!')
        quit()

    symbol_contour = max(contours, key=cv.contourArea)
    x, y, w, h = cv.boundingRect(symbol_contour)

    # Approximate corner points of the symbol card
    peri = cv.arcLength(symbol_contour, True)
    approx = cv.approxPolyDP(symbol_contour, 0.01 * peri, True)
    pts = np.float32(approx)

    # Flatten image to extract symbol card
    symbol_card = flatten_image(image, pts, w, h)
    cv.imshow("card", symbol_card)

    symbol_card_blur = cv.GaussianBlur(symbol_card, (5, 5), 0)
    _, symbol_thresh = cv.threshold(symbol_card_blur, threshold, 255, cv.THRESH_BINARY)
    _, symbol_thresh_inv = cv.threshold(symbol_card_blur, threshold, 255, cv.THRESH_BINARY_INV)

    print('Press "s" to save and continue.')
    key = cv.waitKey(0) & 0xFF
    if key == ord('s'):
        cv.imwrite(IMG_DIR + '/' + filename, symbol_thresh)
        print('Success: Saved image for ' + filename)
    else:
        print('Notice: Skipped over ' + filename)
    
cv.destroyAllWindows()
camera.close()
