import serial
import time
from src.Logger import Logger

log = Logger()

# Will need to figure out how to get name of port for which Arduino USB is connected to

class Arduino:
    def __init__(self, port):
        self.port = port
        self.baud_rate = 0
        self.connection = None

    def connect(self):
        log.info('Attempting connection with Arduino')
        try:
            self.connection = serial.Serial(port, self.baud_rate, timeout=3)
            time.sleep(3)

            if self.connection is not None:
                log.info('Successfully connected with Arduino')
                self.read()
        except Exception as error:
            log.error(f'Connection with Arduino failed: {error}')
    
    def write(self, msg):
        try:
            self.connection.write(msg)
            log.info('Successfully wrote message to Arduino')
        except Exception as error:
            log.error(f'Arduino write failed: {error}')

    def read(self):
        try:
            msg = self.connection.readline()
            return msg            
        except Exception as error:
            log.error(f'Arduino read failed: {error}')