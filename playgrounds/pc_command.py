from src.communicator.PC import PC
import time

pc = PC()
pc.connect()

while True:
    command = input("Enter command to send to PC:")
    pc.write(command)
