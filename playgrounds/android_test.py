from src.communicator.Android import Android
import time
import json

android = Android()
android.connect()

while True:
    # Send a status message
    message = {'bot_status':'Moving'}
    android.write(json.dumps(message))
    time.sleep(1)
    pass
