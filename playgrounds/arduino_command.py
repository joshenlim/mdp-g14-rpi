from src.communicator.Arduino import Arduino

arduino = Arduino()
arduino.connect()

while True:
    command = input("Enter command to send to Arduino:")
    arduino.write(command)
