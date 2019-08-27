from src.communicator.MultiThread import MultiThread
# from src.detector.SymbolDetector import SymbolDetector
from src.Logger import Logger

log = Logger()

def init():
    try:
        multi_thread = MultiThread()
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
