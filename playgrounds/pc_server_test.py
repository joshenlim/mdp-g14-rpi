from src.communicator.PC import PC


pc = PC()
pc.connect()

while True:
    msg = pc.read()
    if msg is not None:
        print('Message from PC: ' + str(msg))
