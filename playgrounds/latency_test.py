import time
from datetime import datetime
from src.communicator.Arduino import Arduino

arduino = Arduino()


arduino.connect()

while True:
	arduino.write('w1')
	
	movement_start = datetime.now()

	msg = arduino.read()
	if msg is not None:
		print('Message from Arduino:' + str(msg))
		if msg == 'MC':
			movement_end = datetime.now()
		
			total_time = movement_end - movement_start
			print('Total time: ' + str(total_time))
			
	
