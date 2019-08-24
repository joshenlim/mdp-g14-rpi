import cv2 as cv
import numpy as np
import time
import os

from src.config import CAMERA_RES_WIDTH
from src.config import CAMERA_RES_HEIGHT
from src.config import CAMERA_FRAMERATE
from src.config import IMG_DIR
from src.config import MATCH_THRESHOLD

from src.detector.utils import preprocess_frame
from src.detector.utils import extract_extreme_points
from src.detector.utils import extract_detected_symbol_thresh

from src.detector.VideoStream import VideoStream
from src.detector.Symbols import load_symbols
from src.Logger import Logger

log = Logger()
font = cv.FONT_HERSHEY_SIMPLEX

class SymbolDetector:
    def __init__(self, width=CAMERA_RES_WIDTH, height=CAMERA_RES_HEIGHT, framerate=CAMERA_FRAMERATE):
        log.info('Initializing Symbol Detector and PiCamera')
        self.video_stream = VideoStream((width, height), framerate)
        self.train_symbols = load_symbols(IMG_DIR)
        self.cam_quit = 0

    def detect(self):
        self.video_stream.start()
        time.sleep(3)
        log.info('Detecting for Symbols')
        while self.cam_quit == 0:
            image = self.video_stream.read()
            pre_proc_frame = preprocess_frame(image)
            _, contours, hierarchy = cv.findContours(pre_proc_frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv.contourArea, reverse=True)

            if len(contours) > 1:
                symbol_contour = contours[1]
                cv.drawContours(image, [symbol_contour], -1, (0, 255, 0), 3)
                
                x, y, w, h = cv.boundingRect(symbol_contour)

                extLeft, extTop, extRight, extBottom = extract_extreme_points(symbol_contour)

                cv.rectangle(image, (extLeft[0], extTop[1]), (extRight[0], extBottom[1]), (0, 255, 0), 2)

                symbol_thresh = extract_detected_symbol_thresh(image, extLeft, extTop, extRight, extBottom)

                cv.imshow("Detected Object", symbol_thresh)

                match_results = []

                for train_symbol in self.train_symbols:
                    train_symbol_gray = cv.cvtColor(train_symbol.img, cv.COLOR_BGR2GRAY)
                    _, train_symbol_thresh = cv.threshold(train_symbol_gray, 127, 255, 0)
                    _, train_symbol_ctrs, _ = cv.findContours(train_symbol_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                    train_symbol_ctrs = sorted(train_symbol_ctrs, key=cv.contourArea, reverse=True)
                    train_symbol_ctr = train_symbol_ctrs[0]
            
                    match_score = cv.matchShapes(symbol_contour, train_symbol_ctr, 1, 0.0)
                    match_results.append({
                        'score': match_score,
                        'symbol': train_symbol.name,
                        'img': train_symbol.img,
                        'id': train_symbol.id
                    })

                closest_match = min(match_results, key=lambda x: x['score'])
                if closest_match['score'] < MATCH_THRESHOLD:
                    cv.imshow('Matching Symbol', closest_match['img'])
                    cv.putText(
                        image,
                        'Symbol: ' + str(closest_match['symbol']) + '; ID: ' + str(closest_match['id']),
                        (extLeft[0], extTop[1] - 20),
                        font,
                        1.0,
                        (0, 255, 0)
                    )
                    print('Found: ' + str(closest_match['symbol']) + '; Image ID: ' + str(closest_match['id']))

            cv.imshow("Video Stream", image)
            key = cv.waitKey(1) & 0xFF

    def end(self):
        self.cam_quit = 1
        cv.destroyAllWindows()
        self.video_stream.stop()
        log.info('Symbol Detector Closed')
