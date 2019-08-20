import cv2
import os
import numpy as np

'''
Example of how Contour Matching works
Compare the contours (outlines) of two given images
The lower the ret value, the greater the similarity
Contour Matching also has a pretty good tolerance against
angle of rotation too
'''

TRAIN_IMG = '/home/pi/Desktop/mdp-g14-rpi/playgrounds/test.jpg'
MATCH_IMG = '/home/pi/Desktop/mdp-g14-rpi/images/4.jpg'

img = cv2.imread(TRAIN_IMG)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, img_thresh = cv2.threshold(img_gray, 127, 255, 0)

img_copy = cv2.imread(MATCH_IMG)
img_copy_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
_, img_copy_thresh = cv2.threshold(img_copy_gray, 127, 255, 0)

_, contours, _ = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)
symbol_ctr = contours[0]

_, contours_copy, _ = cv2.findContours(img_copy_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_copy = sorted(contours_copy, key=cv2.contourArea, reverse=True)
symbol_ctr_copy = contours_copy[0]

ret = cv2.matchShapes(symbol_ctr, symbol_ctr_copy, 1, 0.0)
print(ret)

cv2.drawContours(img, [symbol_ctr], -1, (0, 255, 0), 3)
cv2.imshow('img', img)
cv2.drawContours(img_copy, [symbol_ctr_copy], -1, (0, 0, 255), 3)
cv2.imshow('img2', img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
