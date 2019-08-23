import _thread
import queue
import os

from src.Logger import Logger
from src.communicator.Arduino import Arduino

log = Logger()

'''
TO-DO: Relook at readAndroid, writeAndroid,readPc and writePc
once the classes are up. Figure out if this multithread is working
'''

class MultiThread:
    def __init__(self):
        log.info('Initializing Multithread Communication')
        self.android = None
        self.arduino = Arduino()
        self.pc = None

        # self.android.connect()
        # self.arduino.connect()
        # self.pc.connect()

        self.androidQueue = queue.Queue(maxsize= 0)
        self.arduinoQueue = queue.Queue(maxsize=0)
        self.pcQueue = queue.Queue(maxsize=0)

    def start(self):
        # _thread.start_new_thread(self.readAndroid, ())
        # _thread.start_new_thread(self.readArduino, ())
        # _thread.start_new_thread(self.readPc,())

        # _thread.start_new_thread(self.writeAndroid, (self.androidQueue))
        # _thread.start_new_thread(self.writeArduino, (self.arduinoQueue))
        # _thread.start_new_thread(self.writePc, (self.pcQueue))
        log.info('Multithread Communication Session Started')

        while True:
            pass

    def end(self):
        # self.android.disconnect()
        # self.arduino.disconnect()
        # self.pc.disconnect()
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
