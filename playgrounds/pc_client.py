import socket
import sys
import time

'''
Just note that sending of messages has to be within the same session
'''

host = '192.168.3.1'
port = 3053

print('# Creating socket')
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

print('# Getting remote IP address') 
try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()

# Connect to remote server
print('# Connecting to server, ' + host + ' (' + remote_ip + ')')
s.connect((remote_ip , port))

# Send data to remote server
while True:
    time.sleep(5)
    print('# Sending data to server')
    msg = "Hello from yo\n"

    try:
        s.sendall(msg.encode('utf-8'))
    except socket.error:
        print ('Send failed')
        sys.exit()

# Receive data
# print('# Receive data from server')
# reply = s.recv(1024)

# print('reply: ' + reply.strip().decode("UTF-8")) 