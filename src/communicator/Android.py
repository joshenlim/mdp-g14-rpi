import bluetooth

class Android():
    def __init__(self):
        pass
        
    def setupConnection(self):
        try:
            log.info('Setting up Bluetooth Connection')
            self.server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

            port = bluetooth.get_available_port( bluetooth.RFCOMM ) # get any available bt port
            #port = 5 #hardcoded
            self.server_sock.bind(("",port))
            self.server_sock.listen(1)
            log.info("Waiting on port: " % port)

            uuid = "00000000-0000-1000-8000-00805F9B34FC"  # client need to have same uuid? 
            bluetooth.advertise_service( self.server_sock, 
                            "My Server", uuid ,
                            service_classes = [ uuid, SERIAL_PORT_CLASS ],
                                      profiles = [ SERIAL_PORT_PROFILE ],)

            self.client_sock,address = server_sock.accept()
            log.info("Connected to Android Table at address: ",address)

        except Exception, e:	
            log.error("Error setting up a connection")
            self.client_sock.close()
            self.server_sock.close()
        
    def receive(self):
        try:
            data = self.client_sock.recv(1024)
            log.info("received [%s]" % data)
        except Exception, e:	
            log.error("Error Receiving data")
      
      
      
    def send(self, message):
        try:
            log.info("sending ", message)
            self.server_sock.send(message)
        except Exception, e:	
            log.error("Error sending message ", message)

    def endConnection(self):
        try:
            self.client_sock.close()
            self.server_sock.close()
            log.info("Disconnected Successfully")
        except Exception, e:	
            log.error("Error Disconnecting")