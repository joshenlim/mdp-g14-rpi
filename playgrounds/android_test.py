from src.communicator.Android import Android
import time
import json
import random

statuses = ['moving', 'stopped', 'turning', 'ready', 'completed']

symbol_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

android = Android()
android.connect()

# android.write("MDF|FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF|010002000400000000000043F0800100000003C08081000200080020F880100000000000040|N|18|1|0")
android.write("F|LLS4RS5RS4LS9S3")
while True:
    '''
    for status in statuses:
        message = {'bot_status' : status}
        android.write(json.dumps(message))
        time.sleep(1)
    '''
    
    '''
    for symbol_id in symbol_ids:
        rand_x = random.randint(0, 15)
        rand_y = random.randint(0, 20)
        message = {
            'symbol_id' : symbol_id,
            'coordinate' : str(rand_x) + "," + str(rand_y)
        }
        android.write(json.dumps(message))
        time.sleep(1)
    '''
    msg = android.read()
    if msg is not None:
        print('message from android: ' + str(msg))
