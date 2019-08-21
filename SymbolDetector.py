import cv2 as cv
import numpy as np
import time
import os

from config import CAMERA_RES_WIDTH
from config import CAMERA_RES_HEIGHT
from config import CAMERA_FRAMERATE
from config import IMG_DIR
from config import MATCH_THRESHOLD
from utils import preprocess_frame
import VideoStream
import Symbols

video_stream = VideoStream.VideoStream((CAMERA_RES_WIDTH, CAMERA_RES_HEIGHT), CAMERA_FRAMERATE).start()
train_symbols = Symbols.load_symbols(IMG_DIR)

print('Initializing PiCamera...')
time.sleep(3)
cam_quit = 0

# Create a main.py, remove playgrounds
# Assumingly will have folders for rpi
# one for symbol detection, the other for communication
# ultimately main.py should establish communication and
# init symbol detection process
# wrap everything accordingly

print('Detecting for Symbols - press "q" to quit')

while cam_quit == 0:
    image = video_stream.read()
    pre_proc_frame = preprocess_frame(image)
    _, contours, hierarchy = cv.findContours(pre_proc_frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)
    
    if len(contours) > 1:
        '''
        Grab the second largest contour area as the symbol
        Assumingly, background noise will take the largest
        area from the camera's perspective, but retweak
        during the actual run in the maze itself.
        '''
        symbol = contours[1]
        x, y, w, h = cv.boundingRect(symbol)

        peri = cv.arcLength(symbol, True)
        approx = cv.approxPolyDP(symbol, 0.01 * peri, True)
        pts = np.float32(approx)

        cv.drawContours(image, [symbol], -1, (0, 255, 0), 3)

        # Extract out into a method: extractExtremePoints
        extLeft = tuple(symbol[symbol[:, :, 0].argmin()][0])
        extRight = tuple(symbol[symbol[:, :, 0].argmax()][0])
        extTop = tuple(symbol[symbol[:, :, 1].argmin()][0])
        extBottom = tuple(symbol[symbol[:, :, 1].argmax()][0])

        # Extract out into a method: drawBoundingPoints
        cv.circle(image, (extLeft[0], extTop[1]), 8, (0, 255, 0), 2)
        cv.circle(image, (extRight[0], extTop[1]), 8, (0, 255, 0), 2)
        cv.circle(image, (extRight[0], extBottom[1]), 8, (0, 255, 0), 2)
        cv.circle(image, (extLeft[0], extBottom[1]), 8, (0, 255, 0), 2)

        # Extract out into a method: viewExtractedThreshold
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

        match_results = []

        for train_symbol in train_symbols:
            train_symbol_gray = cv.cvtColor(train_symbol.img, cv.COLOR_BGR2GRAY)
            _, train_symbol_thresh = cv.threshold(train_symbol_gray, 127, 255, 0)
            _, train_symbol_ctrs, _ = cv.findContours(train_symbol_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            train_symbol_ctrs = sorted(train_symbol_ctrs, key=cv.contourArea, reverse=True)
            train_symbol_ctr = train_symbol_ctrs[0]
            
            match_score = cv.matchShapes(symbol, train_symbol_ctr, 1, 0.0)
            match_results.append({
                'score': match_score,
                'symbol': train_symbol.name,
                'img': train_symbol.img,
                'id': train_symbol.id
            })

        closest_match = min(match_results, key=lambda x: x['score'])
        if closest_match['score'] < MATCH_THRESHOLD:
            cv.imshow('Matching Symbol', closest_match['img'])
            print('Found: ' + str(closest_match['symbol']) + '; Image ID: ' + str(closest_match['id']))
            # Am thinking, to improve accuracy, only conclude after closest match is the same
            # for 5 consecutive times. Thereafter ping Android
    
    cv.imshow("Symbol Detector", image)

    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = 1
        
cv.destroyAllWindows()
video_stream.stop()
