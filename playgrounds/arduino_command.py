from src.communicator.Arduino import Arduino
from src.communicator.utils import pcMsgParser

arduino = Arduino()
arduino.connect()

# msg_read = "FP|(1,1,N);(2,1,N);(2,2,E)"
# pc_msg = pcMsgParser(msg_read)
# print(pc_msg)

while True:
    '''
    try:
        msg = arduino.read()
        if msg is not None:
            print(msg)
    except Exception as e:
        pass
    '''
    command = input("Enter command to send to Arduino:")
    '''
    if command == 'demo':
        print('Init demo')
        arduino.write(pc_msg['payload']['arduino'])
    else:
    '''
    arduino.write(command)
