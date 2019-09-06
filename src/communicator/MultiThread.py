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

Will need to figure out the communication path between devices, hence the queue
implementations - a message from the PC will have to be passed to the Arduino
so perhaps, read from PC will be pushed to ArduinoQueue (assuming no preprocessing
required on rpi side)
'''

class MultiThread:
    def __init__(self):
        log.info('Initializing Multithread Communication')
        self.android = Android()
        self.arduino = Arduino()
        self.pc = PC()
        # self.detector = SymbolDetector()

        self.android.connect()
        self.arduino.connect()
        self.pc.connect()

        self.android_queue = queue.Queue(maxsize= 0)
        self.arduino_queue = queue.Queue(maxsize=0)
        self.pc_queue = queue.Queue(maxsize=0)

    def start(self):
        # Currently configured to pass messages between android and PC
        # And read write to and fro android
        _thread.start_new_thread(self.read_android, (self.android_queue,))
        _thread.start_new_thread(self.read_arduino, (self.pc_queue,))
        _thread.start_new_thread(self.read_pc,(self.arduino_queue,))

        _thread.start_new_thread(self.write_android, (self.android_queue,))
        _thread.start_new_thread(self.write_arduino, (self.arduino_queue,))
        _thread.start_new_thread(self.write_pc, (self.pc_queue,))

        # _thread.start_new_thread(self.detector.detect, ())

        log.info('Multithread Communication Session Started')

        while True:
            pass

    def end(self):
        # self.detector.end()
        log.info('Multithread Communication Session Ended')

    def read_android(self, android_queue):
        while True:
            msg = self.android.read()
            if msg is not None:
                log.info('Read Android:' + str(msg))
                android_queue.put_nowait('Hello from PC: ' + str(msg))

    def write_android(self, android_queue):
        while True:
            if not android_queue.empty():
                msg = android_queue.get_nowait()
                self.android.write(msg)
                log.info('Write Android: ' + str(msg))

    def read_arduino(self, pc_queue):
        while True:
            msg = self.arduino.read()
            if msg is not None:
                log.info('Read Arduino: ' + str(msg))
                pc_queue.put_nowait(msg)

    def write_arduino(self, arduino_queue):
        while True:
            if not arduino_queue.empty():
                msg = arduino_queue.get_nowait()
                self.arduino.write(msg)
                log.info('Write Arduino: ' + str(msg))

    def read_pc(self, arduino_queue):
        while True:
            msg = self.pc.read()
            if msg is not None:
                log.info('Read PC: ' + str(msg))
                arduino_queue.put_nowait(msg)

    def write_pc(self, pc_queue):
        while True:
            if not pc_queue.empty():
                msg = pc_queue.get_nowait()
                self.pc.write(msg)
                log.info('Write PC: ' + str(msg))
