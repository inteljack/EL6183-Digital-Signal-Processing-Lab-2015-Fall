#!/usr/local/bin/python
################################################################
# A Python script to download and build Python's source code.
# Uses getfile.py, a utility module which encapsulates ftp step.
################################################################

import getfile
Version = '1.5'                         # version to download
tarname = 'python%s.tar.gz' % Version   # remote/local file name

# fetch with utility 
getfile.getfile(tarname, 'ftp.python.org', 'pub/python/src')

# rest is the same
execfile('buildPython.py')
