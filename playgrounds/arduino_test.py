from src.communicator.Arduino import Arduino

arduino = Arduino()
arduino.connect()
arduino.show_settings()

while True:
    #write_msg = input('Input character to send to Arduino:')
    #print('Sending to Arduino: ' + str(write_msg))
    #arduino.write(write_msg)

    msg = arduino.read()
    print('Message from Arduino: ' + str(msg))
