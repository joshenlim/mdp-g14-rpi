from src.communicator.MultiThread import MultiThread
from src.detector.SymbolDetector import SymbolDetector
from src.Logger import Logger

log = Logger()

def init():
    '''
    I've a feeling detector must be a thread process as well actually
    Check if communication works first, then detector separately
    Then see if all works together in the same session
    '''
    try:
        multi_thread = MultiThread()
        # multi_thread.start()

        # The code will stall here since start loops endlessly

        detector = SymbolDetector()
        detector.detect()
    except KeyboardInterrupt:
        multi_thread.end()
        detector.end()

if __name__ == '__main__':
    init()
