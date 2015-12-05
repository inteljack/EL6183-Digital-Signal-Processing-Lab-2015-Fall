#########################################################
# Server side: open a socket on a port, listen for
# a message from a client, and send an echo reply; 
# this is a simple one-shot listen/reply per client, 
# but it goes into an infinite loop to listen for 
# more clients as long as this server script runs; 
#########################################################

from socket import *                    # get socket constructor and constants
myHost = ''                             # server machine, '' means local host
myPort = 50007                          # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)       # make a TCP socket object
sockobj.bind((myHost, myPort))               # bind it to server port number 
sockobj.listen(5)                            # listen, allow 5 pending connects

while 1:                                     # listen until process killed
    connection, address = sockobj.accept()   # wait for next client connect
    print 'Server connected by', address     # connection is a new socket
    while 1:
        data = connection.recv(1024)         # read next line on client socket
        if not data: break                   # send a reply line to the client
        connection.send('Echo=>' + data)     # until eof when socket closed
    connection.close() 
