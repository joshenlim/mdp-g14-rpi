import bluetooth as bt
from src.Logger import Logger
from src.config import RFCOMM_CHANNEL
from src.config import UUID

log = Logger()

class Android():
    def __init__(self):
        self.server_sock = None
        self.client_sock = None
        pass
        
    def connect(self):
        try:
            log.info('Setting up Bluetooth Connection')
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
            log.info("Successfully connected to Android at address: ", str(address))

        except Exception as error:	
            log.error("Connection with Android failed: " + str(error))
            self.client_sock.close()
            self.server_sock.close()
        
    def read(self):
        try:
            data = self.client_sock.recv(1024)
            log.info("received [%s]" % data)
        except Exception as error:	
            log.error("Android read failed: " + str(error))
      
    def write(self, message):
        try:
            log.info("sending ", message)
            self.server_sock.send(message)
        except Exception as error:	
            log.error("Android write failed " + str(error))

    def disconnect(self):
        try:
            self.client_sock.close()
            self.server_sock.close()
            log.info("Disconnected Successfully")
        except Exception as error:	
            log.error("Android disconnect failed: " + str(error))
