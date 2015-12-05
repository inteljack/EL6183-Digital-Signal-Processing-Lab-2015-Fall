# Echo server program
from socket import *
HOST = ''                         # symbolic name meaning the local host
PORT = 50007                      # arbitrary non-privileged server
s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.send(data)
conn.close()
