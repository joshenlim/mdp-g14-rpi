from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2 as cv
import numpy as np
import time
import os

import Symbols

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

output_dir = os.path.dirname(os.path.abspath(__file__)) + '/images'
# 100 is a good value for BGYW, for red set to 30
threshold = 50

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Allow time for camera to initialize
time.sleep(1)

for name in ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E', 'Arrow', 'Circle']:
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
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    if len(contours) == 0:
        print('Error: No Contours Found!')
        quit()

    symbol_contour = contours[0]
    x, y, w, h = cv.boundingRect(symbol_contour)

    # Approximate corner points of the symbol card
    peri = cv.arcLength(symbol_contour, True)
    approx = cv.approxPolyDP(symbol_contour, 0.01 * peri, True)
    pts = np.float32(approx)

    # Flatten image to extract symbol card
    symbol_card = Symbols.flatten_image(image, pts, w, h)
    cv.imshow("card", symbol_card)

    symbol_card_blur = cv.GaussianBlur(symbol_card, (5, 5), 0)
    _, symbol_thresh = cv.threshold(symbol_card_blur, threshold, 255, cv.THRESH_BINARY)
    _, symbol_thresh_inv = cv.threshold(symbol_card_blur, threshold, 255, cv.THRESH_BINARY_INV)

    cv.imshow("symbol_thresh", symbol_thresh)
    cv.imshow("symbol_thresh_inv", symbol_thresh_inv)

    print('Press "s" to save and continue.')
    key = cv.waitKey(0) & 0xFF
    if key == ord('s'):
        cv.imwrite(output_dir + '/' + filename, symbol_thresh)
        cv.imwrite(output_dir + '_inv/' + filename, symbol_thresh_inv)
        print('Success: Saved image for ' + filename)
    else:
        print('Notice: Skipped over ' + filename)
    
cv.destroyAllWindows()
camera.close()
