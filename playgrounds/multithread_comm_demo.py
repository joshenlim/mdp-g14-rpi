import _thread
import queue
import os

from src.Logger import Logger
from src.communicator.Arduino import Arduino
from src.communicator.PC import PC

log = Logger()

# python3 -m playgrounds.multithread_comm_demo

# 1. Read from 2 sources simultaneuously (x)
# 2. Pass message from PC to Arduino
#    a. Arduino must be reading and writing at the same time
#    b. PC starts by passing an alphabet, Arduino increments it, pass it back

class MultiThread:
    def __init__(self):
        log.info('Initializing Multithread Communication')
        self.arduino = Arduino()
        self.pc = PC()

        self.arduino.connect()
        self.pc.connect()

        self.arduino_queue = queue.Queue(maxsize=0)
        # self.pc_queue = queue.Queue(maxsize=0)

    def start(self):
        _thread.start_new_thread(self.read_arduino, ())
        _thread.start_new_thread(self.read_pc,())

        # _thread.start_new_thread(self.write_arduino, (self.arduino_queue))
        # _thread.start_new_thread(self.write_pc, (self.pc_queue))

        log.info('Multithread Communication Session Started')

        while True:
            pass

    def end(self):
        log.info('Multithread Communication Session Ended')

    def read_arduino(self):
        while True:
            msg = self.arduino.read()
            log.info('Read Arduino: ' + str(msg))

    def write_arduino(self, arduino_queue):
        '''
        This is assuming that a message will be initially
        written to the Arduino Queue.
        '''
        while True:
            if not arduino_queue.empty():
                msg = arduino_queue.get_nowait()
                self.arduino.write(msg)
                log.info('Write Arduino: ' + str(msg))

    def read_pc(self):
        while True:
            msg = self.pc.read()
            if msg is not None:
                log.info('Read PC: ' + str(msg))

    def write_pc(self, pc_queue):
        while True:
            if not pc_queue.empty():
                msg = pc_queue.get_nowait()
                self.pc.write(msg)
                log.info('Write PC: ' + str(msg))

multithread = MultiThread()
multithread.start()
