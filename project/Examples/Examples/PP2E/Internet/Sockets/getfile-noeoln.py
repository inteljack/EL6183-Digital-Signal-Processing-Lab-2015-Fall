###########################################################
# OLD: same as getfile.py, but filenames not sent in a line
###########################################################

import sys, os, thread, time
from socket import *
def now(): return time.ctime(time.time())

blksz  = 1024
myHost = 'localhost'
myPort = 50001

helptext = """
Usage...
server=> getfile.py  -mode server            [-port nnn] [-host hhh|localhost]
client=> getfile.py [-mode client] -file fff [-port nnn] [-host hhh|localhost]
"""

def parsecommandline():
    dict = {}                 # package in a dictionary for easy reference
    args = sys.argv[1:]       # skip program name at front of args list
    while len(args) >= 2:
        dict[args[0]] = args[1]
        args = args[2:]
    return dict

def client(args):
    filename = args.get('-file')
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((myHost, myPort)) 
    sock.send(filename)
    file = open(os.path.split(filename)[1], 'wb')
    while 1:
        data = sock.recv(blksz)            # get up to 1K at a time
        if not data: break                 # till closed on server side
        file.write(data)                   # store data in local file
    sock.close()
    file.close()
    print 'Client got', filename, 'at', now()
    
def serverthread(clientsock):
    filename = clientsock.recv(blksz)      # get filename--not in a line
    try:
        file = open(filename, 'rb')
        while 1:
            bytes = file.read(blksz)       # read/send 1K at a time
            if not bytes: break            # until file totally sent
            sent = clientsock.send(bytes)
            assert sent == len(bytes)
    except:
        print 'Error downloading file on server:', filename
    clientsock.close()
        
def server(args):
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.bind((myHost, myPort))
    serversock.listen(5)
    while 1:
        clientsock, clientaddr = serversock.accept()
        print 'Server connected by', clientaddr, 'at', now()
        thread.start_new_thread(serverthread, (clientsock,))
        
if __name__ == '__main__':
    args = parsecommandline()
    myHost = args.get('-host', myHost)     # use defaults or args
    myPort = int(args.get('-port', myPort))
    if args.get('-mode') == 'server':      # None if no -mode: client
        server(args)
    elif args.get('-file'):                # client mode needs -file
        client(args)
    else:
        print helptext

