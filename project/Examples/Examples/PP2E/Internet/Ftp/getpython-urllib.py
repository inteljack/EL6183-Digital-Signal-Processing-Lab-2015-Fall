#!/usr/local/bin/python
###################################################################
# A Python script to dowload and build Python's source code
# use higher-level urllib instead of ftplib to fetch file
# urllib supports ftp, http, and gopher protocols, and local files
# urllib also allows downloads of html pages, images, text, etc.;
# see also Python html/xml parsers for web pages fetched by urllib;
###################################################################

import os
import urllib                           # socket-based web tools
Version = '1.5'                         # version to download
tarname = 'python%s.tar.gz' % Version   # remote/local file name
 
remoteaddr = 'ftp://ftp.python.org/pub/python/src/' + tarname
print 'Downloading', remoteaddr

# this works too:
# urllib.urlretrieve(remoteaddr, tarname)

remotefile = urllib.urlopen(remoteaddr)     # returns input file-like object
localfile  = open(tarname, 'wb')            # where to store data locally
localfile.write(remotefile.read())
localfile.close()
remotefile.close()
 
# the rest is the same
execfile('buildPython.py')
