#########################################################
# Server side: open a socket on a port, listen for
# a message from a client, and send an echo reply; 
# echos lines until eof when client closes socket;
# spawns a thread to handle each client connection;
# threads share global memory space with main thread;
# this is more portable than fork--not yet on Windows;
#########################################################

import thread, time
from socket import *                     # get socket constructor and constants
myHost = ''                              # server machine, '' means local host
myPort = 50007                           # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)           # make a TCP socket object
sockobj.bind((myHost, myPort))                   # bind it to server port number
sockobj.listen(5)                                # allow upto 5 pending connects

def now(): 
    return time.ctime(time.time())               # current time on the server

def handleClient(connection):                    # in spawned thread: reply
    time.sleep(5)                                # simulate a blocking activity
    while 1:                                     # read, write a client socket
        data = connection.recv(1024)
        if not data: break
        connection.send('Echo=>%s at %s' % (data, now()))
    connection.close() 

def dispatcher():                                # listen until process killd
    while 1:                                     # wait for next connection,
        connection, address = sockobj.accept()   # pass to thread for service
        print 'Server connected by', address,
        print 'at', now() 
        thread.start_new(handleClient, (connection,))

dispatcher()
