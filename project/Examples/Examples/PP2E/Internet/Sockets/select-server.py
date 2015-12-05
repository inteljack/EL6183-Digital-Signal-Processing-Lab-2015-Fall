#################################################################
# Server: handle multiple clients in parallel with select.
# use the select module to multiplex among a set of sockets:
# main sockets which accept new client connections, and 
# input sockets connected to accepted clients; select can
# take an optional 4th arg--0 to poll, n.m to wait n.m secs, 
# ommitted to wait till any socket is ready for processing.
#################################################################

import sys, time
from select import select
from socket import socket, AF_INET, SOCK_STREAM
def now(): return time.ctime(time.time())

myHost = ''                             # server machine, '' means local host
myPort = 50007                          # listen on a non-reserved port number
if len(sys.argv) == 3:                  # allow host/port as cmdline args too
    myHost, myPort = sys.argv[1:]
numPortSocks = 2                        # number of ports for client connects

# make main sockets for accepting new client requests
mainsocks, readsocks, writesocks = [], [], []
for i in range(numPortSocks):
    portsock = socket(AF_INET, SOCK_STREAM)   # make a TCP/IP spocket object
    portsock.bind((myHost, myPort))           # bind it to server port number
    portsock.listen(5)                        # listen, allow 5 pending connects
    mainsocks.append(portsock)                # add to main list to identify
    readsocks.append(portsock)                # add to select inputs list 
    myPort = myPort + 1                       # bind on consecutive ports 

# event loop: listen and multiplex until server process killed
print 'select-server loop starting'
while 1:
    #print readsocks
    readables, writeables, exceptions = select(readsocks, writesocks, [])
    for sockobj in readables:
        if sockobj in mainsocks:                     # for ready input sockets
            # port socket: accept new client
            newsock, address = sockobj.accept()      # accept should not block
            print 'Connect:', address, id(newsock)   # newsock is a new socket
            readsocks.append(newsock)                # add to select list, wait
        else:
            # client socket: read next line
            data = sockobj.recv(1024)                # recv should not block
            print '\tgot', data, 'on', id(sockobj)
            if not data:                             # if closed by the clients 
                sockobj.close()                      # close here and remv from
                readsocks.remove(sockobj)            # del list else reselected 
            else:
                # this may block: should really select for writes too
                sockobj.send('Echo=>%s at %s' % (data, now()))
 
