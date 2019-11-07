import _thread
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

class MultiThread:
    def __init__(self):
        log.info('Initializing Multithread Communication')
        # self.android = Android()
        # self.arduino = Arduino()
        # self.pc = PC()
        self.detector = SymbolDetector()

        # self.android.connect()
        # self.arduino.connect()
        # self.pc.connect()

        self.android_queue = queue.Queue(maxsize= 0)
        self.arduino_queue = queue.Queue(maxsize=0)
        self.pc_queue = queue.Queue(maxsize=0)

    def start(self):
        self.detector.start()
        
        # _thread.start_new_thread(self.read_android, (self.pc_queue,))
        # _thread.start_new_thread(self.read_arduino, (self.pc_queue,))
        # _thread.start_new_thread(self.read_pc,(self.android_queue, self.arduino_queue,))

        # _thread.start_new_thread(self.write_android, (self.android_queue,))
        # _thread.start_new_thread(self.write_arduino, (self.arduino_queue,))
        # _thread.start_new_thread(self.write_pc, (self.pc_queue,))

        _thread.start_new_thread(self.detect_symbols, (self.android_queue,))

        log.info('Multithread Communication Session Started')

        while True:
            pass

    def end(self):
        self.detector.end()
        log.info('Multithread Communication Session Ended')

    def read_android(self, pc_queue):
        while True:
            try:
                msg = self.android.read()
                if msg is not None:
                    log.info('Read Android:' + str(msg))
                    pc_queue.put_nowait(msg)
                    # if msg == 'SV':
                    #   arduino_queue.put_nowait(msg)
                    
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

    def detect_symbols(self, android_queue):
        while True:
            frame = self.detector.get_frame()
            print(frame[0][0])
            time.sleep(2)
            '''
            symbol_match = self.detector.detect(frame)
            if symbol_match is not None:
                print('Symbol Match ID: ' + str(symbol_match))
                android_queue.put_nowait('SID|' + str(symbol_match))
            '''
                    
mt = MultiThread()
mt.start()
