# Echo client program
from socket import *
HOST = 'daring.cwi.nl'            # the remote host
PORT = 50007                      # the same port as used by the server
s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))
s.send('Hello, world')
data = s.recv(1024)
s.close()
print 'Received', `data`
