from src.communicator.Android import Android
import time
import json

statuses = ['moving', 'stopped', 'turning', 'ready', 'completed']

symbol_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

android = Android()
android.connect()

while True:
    for status in statuses:
        message = {'bot_status' : status}
        android.write(json.dumps(message))
        time.sleep(1)
        
    for symbol_id in symbol_ids:
        message = {'symbol_id' : symbol_id}
        android.write(json.dumps(message))
        time.sleep(1)
