import _thread
import queue
import os
import time

'''
Multithreading: _thread.start_new_thread(function, args[, kwargs])
'''

def test_thread(name, delay):
    while True:
        time.sleep(delay)
        print('%s Ping' % (name))
    

class Multithread:
    def __init__(self):
        print('Init Multithread')
        self.run = False

    def start(self):
        print('Begin Multithread Session')
        self.run = True
        _thread.start_new_thread(test_thread, ('Thread 1', 1))
        _thread.start_new_thread(test_thread, ('Thread 2', 2))
        _thread.start_new_thread(test_thread, ('Thread 3', 4))
        print('Multithread Started')

    def end(self):
        print('End Multithread Session')
        self.run = False

mt = Multithread()
mt.start()

while mt.run:
    try:
        pass
    except KeyboardInterrupt:
        mt.end()
    

    
