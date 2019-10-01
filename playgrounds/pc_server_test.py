from src.communicator.PC import PC
from src.communicator.Android import Android
import time

#android = Android()
#android.connect()

pc = PC()
pc.connect()



while True:
    msg = pc.read()
    if msg is not None:
        print('Message from PC:' + str(msg))
        #android.write(msg)
