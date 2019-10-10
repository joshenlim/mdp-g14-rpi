import os

# Using Multiprocess instead of Multithread to employ all 4 cores of RPI
# from src.communicator.MultiThread import MultiThread
from src.communicator.MultiProcess import MultiProcess
# from src.detector.SymbolDetector import SymbolDetector
from src.Logger import Logger

log = Logger()

def init():
    os.system("sudo hciconfig hci0 piscan")
    try:
        multi_thread = MultiProcess()
        multi_thread.start()

        # Currently SymbolDetector seems to be running really slow
        # on a thread. So if just testing SymbolDetector, comment and
        # uncomment respectively the code above and below
        
        # detector = SymbolDetector()
        # detector.detect()
    except KeyboardInterrupt:
        multi_thread.end()
        # detector.end()

if __name__ == '__main__':
    init()
