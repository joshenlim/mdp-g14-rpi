import _thread

from multiprocessing import Process, Queue
import queue
import os
import cv2 as cv
import time

from src.Logger import Logger
from src.detector.SymbolDetector import SymbolDetector
from src.communicator.Arduino import Arduino
from src.communicator.PC import PC
from src.communicator.Android import Android

log = Logger()

'''
Multiprocess to use all available cores on the Rpi
Higher efficiency than multithreading
'''

class MultiProcess:
    def __init__(self):
        log.info('Initializing Multithread Communication')
        self.android = Android()
        self.arduino = Arduino()
        self.pc = PC()
        self.detector = SymbolDetector()

        self.android.connect()
        self.arduino.connect()
        self.pc.connect()

        self.android_queue = Queue()
        self.arduino_queue = Queue()
        self.pc_queue = Queue()
        self.detector_queue = Queue()

        self.frame_count = 0

    def start(self):
        self.detector.start()
        time.sleep(3)
        
        r_android = Process(target=self.read_android, args=(self.pc_queue, self.detector_queue,)).start()
        w_android = Process(target=self.write_android, args=(self.android_queue,)).start()

        r_arduino = Process(target=self.read_arduino, args=(self.pc_queue,)).start()
        w_arduino = Process(target=self.write_arduino, args=(self.arduino_queue,)).start()
        
        r_pc = Process(target=self.read_pc, args=(self.android_queue, self.arduino_queue,)).start()
        w_pc = Process(target=self.write_pc, args=(self.pc_queue,)).start() 

        symbol_detect = Process(target=self.detect_symbols, args=(self.detector_queue, self.android_queue,)).start()
        log.info('Multithread Communication Session Started')
    
    def end(self):
        self.detector.end()
        log.info('Multithread Communication Session Ended')

    def read_android(self, pc_queue, detector_queue):
        while True:
            try:
                msg = self.android.read()
                if msg is not None:
                    log.info('Read Android:' + str(msg))
                    if msg == 'TP':
                        detector_queue.put_nowait(msg)
                    else:
                        pc_queue.put_nowait(msg)
                    
            except Exception as e:
                log.error("Android read failed: " + str(e))
                self.android.connect()

    def write_android(self, android_queue):
        while True:
            if not android_queue.empty():
                try:
                    msg = android_queue.get_nowait()
                    self.android.write(msg)
                    # log.info('Write Android: ' + str(msg))
                except Exception as e:
                    log.error("Android write failed " + str(e))
                    self.android.connect()

    def read_arduino(self, pc_queue):
        while True:
            msg = self.arduino.read()
            if msg is not None and msg != "Connected":
                log.info('Read Arduino: ' + str(msg))
                pc_queue.put_nowait(msg)

    def write_arduino(self, arduino_queue):
        while True:
            if not arduino_queue.empty():
                msg = arduino_queue.get_nowait()
                self.arduino.write(msg)
                log.info('Write Arduino: ' + str(msg))

    def read_pc(self, android_queue, arduino_queue):
        while True:
            msg = self.pc.read()
            if msg is not None:
                log.info('Read PC: ' + str(msg['target']) + '; ' + str(msg['payload']))
                if msg['target'] == 'android':
                    android_queue.put_nowait(msg['payload'])
                elif msg['target'] == 'arduino':
                    arduino_queue.put_nowait(msg['payload'])
                elif msg['target'] == 'both':
                    android_queue.put_nowait(msg['payload']['android'])
                    arduino_queue.put_nowait(msg['payload']['arduino'])

    def write_pc(self, pc_queue):
        while True:
            if not pc_queue.empty():
                msg = pc_queue.get_nowait()
                self.pc.write(msg)
                log.info('Write PC: ' + str(msg))

    def detect_symbols(self, detector_queue, android_queue):
        while True:
            if not detector_queue.empty():
                msg = detector_queue.get_nowait()
                if msg == 'TP':
                    print('Take photo')
                    frame = self.detector.get_frame()
                    self.frame_count = self.frame_count + 1
                    print(frame[0][0], self.frame_count)
                    
                    # frame = self.detector.get_frame()
                    # self.frame_count = self.frame_count + 1
                    # print(frame[0][0], self.frame_count)
                    # cv.imshow("Video Stream", frame)
                    # key = cv.waitKey(1) & 0xFF
            '''
            frame = self.detector.get_frame()
            symbol_match = self.detector.detect(frame)
            if symbol_match is not None:
                print('Symbol Match ID: ' + str(symbol_match))
                android_queue.put_nowait('SID|' + str(symbol_match))
            '''
                    
