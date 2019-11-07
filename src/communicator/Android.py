import bluetooth as bt
from src.Logger import Logger
from src.config import RFCOMM_CHANNEL
from src.config import UUID
from src.config import LOCALE

log = Logger()

'''
Rapsberry Pi serves as socket server, N7 will need a client socket script
as well to establish connection. Should be able to send and receive messages
via the server/client.

TO-DO: Check if Rpi and N7 is server-client or client-client

android = Android()
android.connect()

import time

while True:
    android.read()
    time.sleep(1000)
'''

class Android():
    def __init__(self):
        self.server_sock = None
        self.client_sock = None
        pass
        
    def connect(self):
        try:
            log.info('Establishing connection with N7 Tablet')
            self.server_sock = bt.BluetoothSocket(bt.RFCOMM)

            self.server_sock.bind(("", RFCOMM_CHANNEL))
            self.server_sock.listen(RFCOMM_CHANNEL)
            
            bt.advertise_service(
                self.server_sock, 
                "Server",
                service_id=UUID,
                service_classes=[UUID, bt.SERIAL_PORT_CLASS],
                profiles=[bt.SERIAL_PORT_PROFILE]
            )
            
            log.info('Waiting connection from RFCOMM Channel')
            self.client_sock, address = self.server_sock.accept()
            log.info("Successfully connected to Android at address: " + str(address))

        except Exception as error:	
            log.error("Connection with Android failed: " + str(error))
            self.client_sock.close()
            self.server_sock.close()
        
    def read(self):
        try:
            msg = self.client_sock.recv(1024).decode(LOCALE)
            if len(msg) > 0:
                return msg
            return None
        except Exception as error:	
            raise
      
    def write(self, message):
        try:
            self.client_sock.send(message)
            # log.info('Successfully wrote to Android: ' + str(message))
        except Exception as error:	
            raise

    def disconnect(self):
        try:
            self.client_sock.close()
            self.server_sock.close()
            log.info("Disconnected Successfully")
        except Exception as error:	
            log.error("Android disconnect failed: " + str(error))
