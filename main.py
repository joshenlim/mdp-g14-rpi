import os
import argparse
from src.communicator.MultiThread import MultiThread
# from src.communicator.MultiProcess import MultiProcess
from src.communicator.MultiProcess_v2 import MultiProcess
from src.Logger import Logger

log = Logger()

parser = argparse.ArgumentParser(description='Main Program for MDP')
parser.add_argument('-v', '--verbose', const=True, default=False, nargs='?')

def init():
    args = parser.parse_args()
    verbose = args.verbose
    os.system("sudo hciconfig hci0 piscan")
    try:
        multi_thread = MultiProcess(verbose)
        multi_thread.start()
    except KeyboardInterrupt:
        multi_thread.end()

if __name__ == '__main__':
    init()
