import cv2 as cv
import numpy as np
import time
import os

from src.config import CAMERA_RES_WIDTH
from src.config import CAMERA_RES_HEIGHT
from src.config import CAMERA_FRAMERATE
from src.config import IMG_DIR
from src.config import MATCH_THRESHOLD
from src.config import MATCH_CONFIDENCE_COUNT

from src.detector.utils import preprocess_frame
from src.detector.utils import extract_extreme_points
from src.detector.utils import extract_detected_symbol_thresh
from src.detector.utils import filter_contour_size
from src.detector.utils import derive_arrow_orientation

from src.detector.VideoStream import VideoStream
from src.detector.Symbol import load_symbols
from src.Logger import Logger

log = Logger()
font = cv.FONT_HERSHEY_DUPLEX

class SymbolDetector:
    def __init__(self, width=CAMERA_RES_WIDTH, height=CAMERA_RES_HEIGHT, framerate=CAMERA_FRAMERATE):
        log.info('Initializing Symbol Detector and PiCamera')
        self.video_stream = VideoStream((width, height), framerate)
        self.train_symbols = load_symbols(IMG_DIR)
        self.match_symbol_id = None
        self.match_count = 0
        self.cam_quit = 0

    def start(self):
        self.video_stream.start()
        time.sleep(3)
        log.info('Starting Video Stream')    

    def get_frame(self):
        return self.video_stream.read()

    def detect(self, image):
        pre_proc_frame = preprocess_frame(image)

        # Uncomment if debugging threshold value
        # cv.imshow('Frame Thresh', pre_proc_frame)
        
        _, contours, hierarchy = cv.findContours(pre_proc_frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv.contourArea, reverse=True)
        # cv.drawContours(image, contours, -1, (0, 0, 255), 3)
        filtered_contours = filter_contour_size(contours)
        cv.drawContours(image, filtered_contours, -1, (255, 0, 0), 3)

        if len(filtered_contours) > 0:
            symbol_contour = filtered_contours[0]
            
            x, y, w, h = cv.boundingRect(symbol_contour)
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            extLeft, extTop, extRight, extBottom = extract_extreme_points(symbol_contour)
            symbol_thresh = extract_detected_symbol_thresh(image, extLeft, extTop, extRight, extBottom)
            # cv.imshow("Detected Object", symbol_thresh)

            match_results = []
            for train_symbol in self.train_symbols:
                match_score = cv.matchShapes(symbol_contour, train_symbol.contour, 1, 0.0)
                match_results.append({
                    'score': match_score,
                    'symbol': train_symbol.name,
                    'id': train_symbol.id
                })

            closest_match = min(match_results, key=lambda x: x['score'])
            if closest_match['score'] < MATCH_THRESHOLD:
                # If detected arrow, further derive arrow orientation
                if closest_match['id'] == 0:
                    # Uncomment if debugging for arrow detection
                    # cv.circle(image, (extLeft[0], extLeft[1]), 8, (0, 0, 255), 2)
                    # cv.circle(image, (extTop[0], extTop[1]), 8, (0, 0, 255), 2)
                    # cv.circle(image, (extRight[0], extRight[1]), 8, (0, 0, 255), 2)
                    # cv.circle(image, (extBottom[0], extBottom[1]), 8, (0, 0, 255), 2)
                    # cv.circle(image, (int(((extLeft[0] + extRight[0]) / 2)), int(((extTop[1] + extBottom[1]) / 2))), 8, (0, 0, 255), 2)

                    arrow_name, arrow_id = derive_arrow_orientation(extLeft, extTop, extRight, extBottom)
                    closest_match['symbol'] = arrow_name
                    closest_match['id'] = arrow_id
                    
                cv.putText(
                    image,
                    'Symbol: ' + str(closest_match['symbol']) + '; ID: ' + str(closest_match['id']),
                    (extLeft[0] - 50, extTop[1] - 20),
                    font,
                    0.8,
                    (0, 255, 0)
                )

                if self.match_symbol_id == closest_match['id']:
                    self.match_count = self.match_count + 1
                    
                else:
                    self.match_symbol_id = closest_match['id']
                    self.match_count = 1
                    
                if (self.match_count == MATCH_CONFIDENCE_COUNT):
                        return(closest_match['id'])
            else:
                self.match_symbol_id = None
                self.match_count = 0

        # Uncomment to visualize stream
        cv.imshow("Video Stream", image)
        key = cv.waitKey(1) & 0xFF

    def end(self):
        self.cam_quit = 1
        cv.destroyAllWindows()
        self.video_stream.stop()
        log.info('Symbol Detector Closed')
