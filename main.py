'''
Should first establish communications with Android and
Arduino, and then start SymbolDetector

Convert SymbolDetector to a class
'''

from src.communicator.MultiThread import MultiThread
from src.Logger import Logger

log = Logger()

def init():
    try:
        multi_thread = MultiThread()
        multi_thread.start()
    except KeyboardInterrupt:
        multi_thread.end()

if __name__ == '__main__':
    init()
