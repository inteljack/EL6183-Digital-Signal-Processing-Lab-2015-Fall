#############################################################
# hack--test port 50008 (didn't plan ahead for select-server)
#############################################################

import sys
from socket import *              # portable socket interface plus constants
serverHost = 'localhost'          # server name, or: 'starship.python.net'
serverPort = 50008                # non-reserved port used by the server

message = ['Hello network world']           # default text to send to server
if len(sys.argv) > 1:
    serverHost = sys.argv[1]                # or server from cmd line arg 1
    if len(sys.argv) > 2:                   # or text from cmd line args 2..n
        message = sys.argv[2:]              # one message for each arg listed

sockobj = socket(AF_INET, SOCK_STREAM)      # make a TCP/IP socket object
sockobj.connect((serverHost, serverPort))   # connect to server machine and port

for line in message:
    sockobj.send(line)                      # send line to server over socket
    data = sockobj.recv(1024)               # receive line from server: up to 1k
    print 'Client received:', `data`

sockobj.close()                             # close socket to send eof to server
