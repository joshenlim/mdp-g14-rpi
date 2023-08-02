import json
import time
from multiprocessing import Process, Queue

from src.detector.SymbolDetector import SymbolDetector

from src.communicator.Android import Android
from src.communicator.Arduino import Arduino
from src.communicator.PC import PC
from src.communicator.utils import format_for
from src.Logger import Logger

log = Logger()

'''
New structure for multiprocessing to have only 2 queues
Image Recognition process to run in main program
'''

class MultiProcess:
    def __init__(self, verbose):
        log.info('Initializing Multiprocessing Communication')
        self.verbose = verbose
        self.android = Android()
        self.arduino = Arduino()
        self.pc = PC()
        self.detector = SymbolDetector()

        self.msg_queue = Queue()
        self.img_queue = Queue()
        
    def start(self):
        try:
            self.android.connect()
            self.arduino.connect()
            self.pc.connect()

            Process(target=self.read_android, args=(self.msg_queue,)).start()
            Process(target=self.read_arduino, args=(self.msg_queue,)).start()
            Process(target=self.read_pc, args=(self.msg_queue, self.img_queue,)).start()
            
            Process(target=self.write_target, args=(self.msg_queue,)).start()

            log.info('Launching Symbol Detector')
            self.detector.start()

            log.info('Multiprocess Communication Session Started')

            while True:
                if not self.img_queue.empty():
                    msg = self.img_queue.get_nowait()
                    if msg == 'TP':
                        log.info('Detecting for Symbols')
                        frame = self.detector.get_frame()
                        symbol_match = self.detector.detect(frame)
                        if symbol_match is not None:
                            log.info('Symbol Match ID: ' + str(symbol_match))
                            self.pc.write('TC|' + str(symbol_match))
                        else:
                            log.info('No Symbols Detected')
                            self.pc.write('TC|0')
        except KeyboardInterrupt:
            raise

    def end(self):
        log.info('Multiprocess Communication Session Ended')

    def read_android(self, msg_queue):
        while True:
            try:
                msg = self.android.read()
                if msg is not None:
                    if self.verbose:
                        log.info('Read Android: ' + str(msg))
                    if msg in ['w1', 'a', 'd', 'h']:
                        msg_queue.put_nowait(format_for('ARD', msg))
                    else:
                        msg_queue.put_nowait(format_for('PC', msg))
                    
            except Exception as e:
                log.error('Android read failed: ' + str(e))
                self.android.connect()

    def read_arduino(self, msg_queue):
        while True:
            msg = self.arduino.read()
            if msg is not None and msg != "Connected":
                if self.verbose:
                    log.info('Read Arduino: ' + str(msg))
                msg_queue.put_nowait(format_for('PC', msg))

    def read_pc(self, msg_queue, img_queue):
        while True:
            msg = self.pc.read()
            if msg is not None:
                if self.verbose:
                    log.info('Read PC: ' + str(msg['target']) + '; ' + str(msg['payload']))
                if msg['target'] == 'android':
                    msg_queue.put_nowait(format_for('AND', msg['payload']))
                elif msg['target'] == 'arduino':
                    msg_queue.put_nowait(format_for('ARD', msg['payload']))
                elif msg['target'] == 'rpi':
                    img_queue.put_nowait(msg['payload'])
                elif msg['target'] == 'both':
                    msg_queue.put_nowait(format_for('AND', msg['payload']['android']))
                    msg_queue.put_nowait(format_for('ARD', msg['payload']['arduino']))

    def write_target(self, msg_queue):
        while True:
            if not msg_queue.empty():
                msg = msg_queue.get_nowait()
                msg = json.loads(msg)
                payload = msg['payload']

                if msg['target'] == 'PC':
                    if self.verbose:
                        log.info('Write PC:' + str(payload))
                    self.pc.write(payload)

                elif msg['target'] == 'AND':
                    if self.verbose:
                        log.info('Write Android:' + str(payload))
                    self.android.write(payload)

                elif msg['target'] == 'ARD':
                    if self.verbose:
                        log.info('Write Arduino:' + str(payload))
                    self.arduino.write(payload)
