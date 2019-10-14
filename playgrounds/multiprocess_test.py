import _thread
import queue
import os
import time

from multiprocessing import Process

'''
Multithreading: _thread.start_new_thread(function, args[, kwargs])
'''

def test_thread(name, delay):
    while True:
        time.sleep(delay)
        print('%s Ping' % (name))
    

class Multiprocess:
    def __init__(self):
        print('Init Multithread')
        self.run = False

    def start(self):
        print('Begin Multithread Session')
        self.run = True
        # _thread.start_new_thread(test_thread, ('Thread 1', 1))
        # _thread.start_new_thread(test_thread, ('Thread 2', 2))
        # _thread.start_new_thread(test_thread, ('Thread 3', 4))
        x1 = Process(target=test_thread, args=('Thread 1', 1))
        x2 = Process(target=test_thread, args=('Thread 2', 2))
        x3 = Process(target=test_thread, args=('Thread 3', 4))

        x1.start()
        x2.start()
        x3.start()

        print('Multiprocess Started')

    def end(self):
        print('End Multithread Session')
        self.run = False

mp = Multiprocess()
mp.start()

while mp.run:
    try:
        pass
    except KeyboardInterrupt:
        mt.end()
    

    
