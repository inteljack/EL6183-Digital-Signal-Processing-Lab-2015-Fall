#!/bin/env python 
###########################################################
# use ftp to copy (download) all files from a remote site
# and directory to a directory on the local machine; e.g., 
# run me periodically to mirror a flat ftp site;
###########################################################

import os, sys, ftplib
from getpass import getpass

remotesite = 'home.rmi.net'
remotedir  = 'public_html'
remoteuser = 'lutz'
remotepass = getpass('Please enter password for %s: ' % remotesite)
localdir   = (len(sys.argv) > 1 and sys.argv[1]) or '.'
if sys.platform[:3] == 'win': raw_input() # clear stream
cleanall   = raw_input('Clean local directory first? ')[:1] in ['y', 'Y']

print 'connecting...'
connection = ftplib.FTP(remotesite)                 # connect to ftp site
connection.login(remoteuser, remotepass)            # login as user/password
connection.cwd(remotedir)                           # cd to directory to copy

if cleanall:
    for localname in os.listdir(localdir):          # try to delete all locals
        try:                                        # first to remove old files
            print 'deleting local', localname
            os.remove(os.path.join(localdir, localname))
        except:
            print 'cannot delete local', localname

count = 0                                           # download all remote files
remotefiles = connection.nlst()                     # nlst() gives files list
                                                    # dir()  gives full details
for remotename in remotefiles:
    localname = os.path.join(localdir, remotename) 
    print 'copying', remotename, 'to', localname
    if remotename[-4:] == 'html' or remotename[-3:] == 'txt':
        # use ascii mode xfer
        localfile = open(localname, 'w')
        callback  = lambda line, file=localfile: file.write(line + '\n')
        connection.retrlines('RETR ' + remotename, callback)
    else:
        # use binary mode xfer
        localfile = open(localname, 'wb')
        connection.retrbinary('RETR ' + remotename, localfile.write)
    localfile.close()
    count = count+1

connection.quit()
print 'Done:', count, 'files downloaded.'
