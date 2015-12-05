#######################################################################
# fetch a file from an http (web) server over sockets via httplib;
# the filename param may have a full directory path, and may name a cgi
# script with query parameters on the end to invoke a remote program;
# fetched file data or remote program output could be saved to a local
# file to mimic ftp, or parsed with string.find or the htmllib module;
#######################################################################

import sys, httplib
showlines = 6
try:
    servername, filename = sys.argv[1:]           # cmdline args?
except:
    servername, filename = 'starship.python.net', '/index.html'

print servername, filename
server = httplib.HTTP(servername)                 # connect to http site/server
server.putrequest('GET', filename)                # send request and headers
server.putheader('Accept', 'text/html')           # POST requests work here too
server.endheaders()                               # as do cgi script file names 

errcode, errmsh, replyheader = server.getreply()  # read reply info headers
if errcode != 200:                                # 200 means success
    print 'Error sending request', errcode
else:
    file = server.getfile()                       # file obj for data received
    data = file.readlines()
    file.close()                                  # show lines with eoln at end
    for line in data[:showlines]: print line,     # to save, write data to file 
