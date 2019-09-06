import _thread
import queue
import os

from src.Logger import Logger
from src.communicator.Android import Android
from src.communicator.Arduino import Arduino
from src.communicator.PC import PC

log = Logger()

# python3 -m playgrounds.multithread_comm_demo

# Demo connects Rpi with Arduino and PC
# Connections established in a sequential fashion
# PC and Arduino will pass alphabets back and forth
# Incrementing the character whenever either device receives a message

class MultiThread:
    def __init__(self):
        log.info('Initializing Multithread Communication')
        self.android = Android()
        self.arduino = Arduino()
        self.pc = PC()

        self.android.connect()
        self.arduino.connect()
        self.pc.connect()

        self.android_queue = queue.Queue(maxsize=0)
        self.arduino_queue = queue.Queue(maxsize=0)
        self.pc_queue = queue.Queue(maxsize=0)

    def start(self):
        _thread.start_new_thread(self.read_android, (self.android_queue,))
        _thread.start_new_thread(self.read_arduino, (self.pc_queue,))
        _thread.start_new_thread(self.read_pc,(self.arduino_queue,))

        _thread.start_new_thread(self.write_android, (self.android_queue,))
        _thread.start_new_thread(self.write_arduino, (self.arduino_queue,))
        _thread.start_new_thread(self.write_pc, (self.pc_queue,))

        log.info('Multithread Communication Session Started')

        while True:
            pass

    def end(self):
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

multithread = MultiThread()
multithread.start()
