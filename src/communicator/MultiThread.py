import _thread
from threading import Thread
import queue
import os
# import cv2 as cv
import time

from src.Logger import Logger
from src.detector.SymbolDetector import SymbolDetector
from src.communicator.Arduino import Arduino
from src.communicator.PC import PC
from src.communicator.Android import Android

log = Logger()
 
'''
Multithreading essentially refers to running multiple processes in parallel
Communications between Rpi and other devices involve a session, which means
the Rpi will be waiting for a trigger. Hence if single threaded, Rpi can only
do one thing at one time. With multhreading, Rpi can have multiple sessions
simultaneuously. Image Recognition will have to be run as a thread as well, but
it seems to be running really slow at the moment. There's also an occasional
error: Camera component couldn't be enabled: Out of resources. If hit that error
just restart the process, wait a little for the resources to be released, then re
run the main program
'''

class MultiThread:
    def __init__(self):
        log.info('Initializing Multithread Communication')
        self.android = Android()
        self.arduino = Arduino()
        self.pc = PC()
        self.detector = SymbolDetector()

        self.android.connect()
        self.arduino.connect()
        self.pc.connect()

        self.android_queue = queue.Queue(maxsize= 0)
        self.arduino_queue = queue.Queue(maxsize=0)
        self.pc_queue = queue.Queue(maxsize=0)
        self.detector_queue = queue.Queue(maxsize=0)

    def start(self):
        # self.detector.start()

        
        _thread.start_new_thread(self.read_android, (self.pc_queue, self.detector_queue))
        _thread.start_new_thread(self.read_arduino, (self.pc_queue,))
        _thread.start_new_thread(self.read_pc,(self.android_queue, self.arduino_queue,))

        _thread.start_new_thread(self.write_android, (self.android_queue,))
        _thread.start_new_thread(self.write_arduino, (self.arduino_queue,))
        _thread.start_new_thread(self.write_pc, (self.pc_queue,))
        
        '''
        Thread(target=self.read_android, args=(self.pc_queue, self.detector_queue,)).start()
        Thread(target=self.read_arduino, args=(self.pc_queue,)).start()
        Thread(target=self.read_pc, args=(self.android_queue, self.arduino_queue,)).start()

        Thread(target=self.write_android, args=(self.android_queue,)).start()
        Thread(target=self.write_arduino, args=(self.arduino_queue,)).start()
        Thread(target=self.write_pc, args=(self.pc_queue,)).start()
        '''
        # _thread.start_new_thread(self.detect_symbols, (self.detector_queue, self.android_queue,))

        log.info('Multithread Communication Session Started')

        while True:
            pass

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
            frame = self.detector.get_frame()
            # print(frame[0][0])
            if not detector_queue.empty():
                # Try match confidence of 1 frame
                # If not good enough, will have to find a way to bump match_confidence
                msg = detector_queue.get_nowait()
                log.info('Detecting Symbols')
                symbol_match = self.detector.detect(frame)
                if symbol_match is not None:
                    log.info('Symbol Match ID: ' + str(symbol_match))
                    android_queue.put_nowait('SID|' + str(symbol_match))
                else:
                    log.info('No symbols detected in frame')
