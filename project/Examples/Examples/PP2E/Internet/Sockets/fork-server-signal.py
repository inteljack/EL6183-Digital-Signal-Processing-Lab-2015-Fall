#########################################################
# Same as fork-server.py, but use the Python signal
# module to avoid keeping child zombie processes after
# they terminate, not an explicit loop before each new 
# connection; SIG_IGN means ignore, and may not work with
# SIG_CHLD child exit signal on all platforms; on Linux,
# socket.accept cannot be interrupted with a signal;
#########################################################

import os, time, sys, signal, signal
from socket import *                      # get socket constructor and constants
myHost = ''                               # server machine, '' means local host
myPort = 50007                            # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)           # make a TCP socket object
sockobj.bind((myHost, myPort))                   # bind it to server port number
sockobj.listen(5)                                # up to 5 pending connects
signal.signal(signal.SIGCHLD, signal.SIG_IGN)    # avoid child zombie processes

def now():                                       # time on server machine
    return time.ctime(time.time())

def handleClient(connection):                    # child process replies, exits
    time.sleep(5)                                # simulate a blocking activity
    while 1:                                     # read, write a client socket
        data = connection.recv(1024)
        if not data: break  
        connection.send('Echo=>%s at %s' % (data, now()))
    connection.close() 
    os._exit(0)

def dispatcher():                                # listen until process killed
    while 1:                                     # wait for next connection,
        connection, address = sockobj.accept()   # pass to process for service
        print 'Server connected by', address,
        print 'at', now()
        childPid = os.fork()                     # copy this process
        if childPid == 0:                        # if in child process: handle
            handleClient(connection)             # else: go accept next connect

dispatcher()
