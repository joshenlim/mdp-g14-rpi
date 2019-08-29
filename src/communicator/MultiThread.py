import _thread
import queue
import os

from src.Logger import Logger
# from src.detector.SymbolDetector import SymbolDetector
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
        # self.detector = SymbolDetector()

        # self.android.connect()
        self.arduino.connect()
        # self.pc.connect()

        self.androidQueue = queue.Queue(maxsize= 0)
        self.arduinoQueue = queue.Queue(maxsize=0)
        self.pcQueue = queue.Queue(maxsize=0)

    def start(self):
        # _thread.start_new_thread(self.readAndroid, ())
        _thread.start_new_thread(self.readArduino, ())
        # _thread.start_new_thread(self.readPc,())

        # _thread.start_new_thread(self.writeAndroid, (self.androidQueue))
        # _thread.start_new_thread(self.writeArduino, (self.arduinoQueue))
        # _thread.start_new_thread(self.writePc, (self.pcQueue))

        # _thread.start_new_thread(self.detector.detect, ())
        log.info('Multithread Communication Session Started')

        while True:
            pass

    def end(self):
        # self.android.disconnect()
        # self.pc.disconnect()
        # self.detector.end()
        log.info('Multithread Communication Session Ended')

    def readAndroid(self):
        while True:
            msg = self.android.read()
            log.info('Read Android:' + str(msg))

    def writeAndroid(self, androidQueue):
        while True:
            if not androidQueue.empty():
                msg = androidQueue.get_nowait()
                self.android.write(msg)
                log.info('Write Android: ' + str(msg))

    def readArduino(self):
        while True:
            msg = self.arduino.read()
            log.info('Read Arduino: ' + str(msg))

    def writeArduino(self, arduinoQueue):
        while True:
            if not arduinoQueue.empty():
                msg = arduinoQueue.get_nowait()
                self.arduino.write(msg)
                log.info('Write Arduino: ' + str(msg))

    def readPc(self):
        while True:
            msg = self.pc.read()
            log.info('Read PC: ' + str(msg))

    def writePc(self, pcQueue):
        while True:
            if not pcQueue.empty():
                msg = pcQueue.get_nowait()
                self.pc.write(msg)
                log.info('Write PC: ' + str(msg))
