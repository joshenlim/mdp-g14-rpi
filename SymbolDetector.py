import cv2 as cv
import numpy as np
import time
import os

from config import CAMERA_RES_WIDTH
from config import CAMERA_RES_HEIGHT
from config import CAMERA_FRAMERATE
from config import IMG_DIR
from utils import preprocess_frame
from utils import perspective_transform
from utils import filter_contours
import VideoStream
import Symbols

frame_rate_calc = 1
freq = cv.getTickFrequency()
font = cv.FONT_HERSHEY_SIMPLEX

video_stream = VideoStream.VideoStream((CAMERA_RES_WIDTH, CAMERA_RES_HEIGHT), CAMERA_FRAMERATE).start()
time.sleep(1)

train_symbols = Symbols.load_symbols(IMG_DIR)

cam_quit = 0

print('Detecting for Symbols - press "q" to quit')
while cam_quit == 0:
    image = video_stream.read()

    pre_proc_frame = preprocess_frame(image)

    _, contours, hierarchy = cv.findContours(pre_proc_frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    # cv.drawContours(image, contours, -1, (255, 0, 0), 3)
    
    if len(contours) > 1:
        symbol = contours[1]
        # print('Area: ' + str(cv.contourArea(symbol)))
        # cv.drawContours(image, symbol, -1, (0, 0, 255), 3)
        x, y, w, h = cv.boundingRect(symbol)

        peri = cv.arcLength(symbol, True)
        approx = cv.approxPolyDP(symbol, 0.01 * peri, True)
        pts = np.float32(approx)

        cv.drawContours(image, [symbol], -1, (0, 255, 0), 3)

        extLeft = tuple(symbol[symbol[:, :, 0].argmin()][0])
        extRight = tuple(symbol[symbol[:, :, 0].argmax()][0])
        extTop = tuple(symbol[symbol[:, :, 1].argmin()][0])
        extBottom = tuple(symbol[symbol[:, :, 1].argmax()][0])

        cv.circle(image, (extLeft[0], extTop[1]), 8, (0, 255, 0), 2)
        cv.circle(image, (extRight[0], extTop[1]), 8, (0, 255, 0), 2)
        cv.circle(image, (extRight[0], extBottom[1]), 8, (0, 255, 0), 2)
        cv.circle(image, (extLeft[0], extBottom[1]), 8, (0, 255, 0), 2)

        placeholder_box = np.zeros((4, 2), dtype="float32")
        placeholder_box[0] = (extLeft[0], extTop[1]) # Top Left
        placeholder_box[1] = (extRight[0], extTop[1]) # Top Right
        placeholder_box[2] = (extRight[0], extBottom[1]) # Bottom Left
        placeholder_box[3] = (extLeft[0], extBottom[1]) # Bottom Right

        placeholder_width = extRight[0] - extLeft[0]
        placeholder_height = extBottom[1] - extTop[1]

        dst = np.array([
            [0,0],
            [placeholder_width - 1, 0],
            [placeholder_width - 1, placeholder_height - 1],
            [0, placeholder_height - 1]
        ], np.float32)
        M = cv.getPerspectiveTransform(placeholder_box, dst)
        warp = cv.warpPerspective(image, M, (placeholder_width, placeholder_height))
        warp = cv.cvtColor(warp, cv.COLOR_BGR2GRAY)

        symbol_card_blur = cv.GaussianBlur(warp, (5, 5), 0)
        _, symbol_thresh = cv.threshold(symbol_card_blur, 100, 255, cv.THRESH_BINARY)

        cv.imshow("Detected Object", symbol_thresh)

        for train_symbol in train_symbols:
            train_symbol_gray = cv.cvtColor(train_symbol.img, cv.COLOR_BGR2GRAY)
            _, train_symbol_thresh = cv.threshold(train_symbol_gray, 127, 255, 0)
            _, train_symbol_ctrs, _ = cv.findContours(train_symbol_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            train_symbol_ctrs = sorted(train_symbol_ctrs, key=cv.contourArea, reverse=True)
            train_symbol_ctr = train_symbol_ctrs[0]
            
            ret = cv.matchShapes(symbol, train_symbol_ctr, 1, 0.0)
            # Further improvement, find min from all the results, check if min is below threshold
            # Surprisingly works well with all colors, red is a bit of a stretch
            # Only thing is the detection of the contours still need to improve
            # And contour matching threshold value
            if (ret < 0.1):
                print('Found: ' + str(train_symbol.name))
    
    cv.imshow("Symbol Detector", image)

    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = 1
        
cv.destroyAllWindows()
video_stream.stop()
