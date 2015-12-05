#!/usr/local/bin/python
###############################################################
# A Python script to download and build Python's source code.
# Uses ftplib, the ftp protocol handler which uses sockets.
# Ftp runs on 2 sockets (one for data, one for control--on
# ports 20 and 21) and imposes message text formats, but the 
# Python ftplib module hides most of this protocol's details.
###############################################################

import os
from ftplib import FTP                   # socket-based ftp tools
Version = '1.5'                          # version to download
tarname = 'python%s.tar.gz' % Version    # remote/local file name
 
print 'Connecting...'
localfile  = open(tarname, 'wb')         # where to store download
connection = FTP('ftp.python.org')       # connect to ftp site
connection.login()                       # default is anonymous login
connection.cwd('pub/python/src')         # xfer 1k at a time to localfile

print 'Downloading...'
connection.retrbinary('RETR ' + tarname, localfile.write, 1024)
connection.quit()
localfile.close()
 
print 'Unpacking...'
os.system('gzip -d '  + tarname)         # decompress
os.system('tar -xvf ' + tarname[:-3])    # strip .gz 

print 'Building...'
os.chdir('Python-' + Version)            # build Python itself
os.system('./configure')                 # assumes unix-style make
os.system('make')
os.system('make test')
print 'Done: see Python-%s/python.' % Version

