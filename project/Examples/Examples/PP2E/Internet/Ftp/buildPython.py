#!/usr/local/bin/python
###############################################################
# A Python script to build Python from its source code.
# Run me in directory where Python source distribution lives.
###############################################################

import os
Version = '1.5'                         # version to build
tarname = 'python%s.tar.gz' % Version   # remote/local file name
 
print 'Unpacking...'
os.system('gzip -d '  + tarname)        # decompress file
os.system('tar -xvf ' + tarname[:-3])   # untar without '.gz'

print 'Building...'
os.chdir('Python-' + Version)           # build Python itself
os.system('./configure')                # assumes unix-style make
os.system('make')
os.system('make test')
print 'Done: see Python-%s/python.' % Version
