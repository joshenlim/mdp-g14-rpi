from multiprocessing import Process, Queue
import queue
import os
import cv2 as cv
import time

from src.Logger import Logger
from src.communicator.PC import PC

log = Logger()

class MultiThread:
    def __init__(self):
        log.info('Initializing Multithread Communication')
        self.pc = PC()
        self.pc.connect()

        self.pc_queue = Queue()

    def start(self):

        read_pc = Process(target=self.read_pc, args=(self.pc_queue,))
        read_pc.start()
        
        write_pc = Process(target=self.write_pc, args=(self.pc_queue,))
        write_pc.start()

    def end(self):
        log.info('Multithread Communication Session Ended')
        
    def read_pc(self, pc_queue):
        print('read read')
        while True:
            msg = self.pc.read()
            if msg is not None:
                print('Received: ' + str(msg))
                pc_queue.put_nowait(msg['payload'])
                '''
                log.info('Read PC: ' + str(msg['target']) + '; ' + str(msg['payload']))
                if msg['target'] == 'android':
                    android_queue.put_nowait(msg['payload'])
                elif msg['target'] == 'arduino':
                    arduino_queue.put_nowait(msg['payload'])
                elif msg['target'] == 'both':
                    android_queue.put_nowait(msg['payload']['android'])
                    arduino_queue.put_nowait(msg['payload']['arduino'])
                '''

    def write_pc(self, pc_queue):
        print('write write')
        while True:
            if not pc_queue.empty():
                msg = pc_queue.get_nowait()
                print('Write: ' + str(msg))
                self.pc.write(msg)
                log.info('Write PC: ' + str(msg))

    def detect_symbols(self, android_queue):
        while True:
            frame = self.detector.get_frame()
            symbol_match = self.detector.detect(frame)
            if symbol_match is not None:
                print('Symbol Match ID: ' + str(symbol_match))
                android_queue.put_nowait('SID|' + str(symbol_match))

mp = MultiThread()
mp.start()
                    
