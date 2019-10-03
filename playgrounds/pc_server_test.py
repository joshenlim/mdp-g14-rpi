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
            print('Message from PC: ' + str(msg))
            time.sleep(0.1)
            pc.write('MC')
    except Exception as e:
        print(e)
