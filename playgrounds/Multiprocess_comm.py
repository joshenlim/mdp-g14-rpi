from multiprocessing import Process, Queue
import queue
import os
import cv2 as cv
import time

from src.Logger import Logger
from src.detector.VideoStream import VideoStream

log = Logger()

class MultiThread:
    def __init__(self):
        log.info('Initializing Multithread Communication')
        self.vid = VideoStream((540, 480), 30)

    def start(self):
        self.vid.start()
        time.sleep(3)
        
        Process(target=self.detect_symbols, args=()).start()
        while True:
            # but this is fine
            print('ff: ' + str(self.vid.read()[0][0]))
            time.sleep(2)
        
    def end(self):
        log.info('Multithread Communication Session Ended')

    def detect_symbols(self):
        while True:
            # frame = self.vid.read()
            # Weird problem that .read() does not update frame
            print('frame:' + str(self.vid.read()[0][0]))
            time.sleep(2)
            # symbol_match = self.detector.detect(frame)
            # if symbol_match is not None:
            #     print('Symbol Match ID: ' + str(symbol_match))
            #     android_queue.put_nowait('SID|' + str(symbol_match))

mp = MultiThread()
mp.start()
                    
