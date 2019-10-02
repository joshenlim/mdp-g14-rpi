from src.communicator.PC import PC
from src.communicator.Android import Android
import time

#android = Android()
#android.connect()

pc = PC()
pc.connect()



while True:
    try:
        msg = pc.read()
        if msg is not None:
            msg = msg.strip()
            print('Message from PC: ' + msg)
            # pc.write('B')
    except Exception as e:
        print(e)
