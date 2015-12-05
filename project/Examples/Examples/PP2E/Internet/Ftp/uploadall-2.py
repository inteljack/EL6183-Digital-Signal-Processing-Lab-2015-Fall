#!/bin/env python
##########################################################################
# like uploadall.py, but doesn't assume topremotedir already exists
##########################################################################

import os, sys, ftplib
from getpass import getpass
fcount = dcount = 0
 
def uploadDir(localdir, remotedir, connection):
    global fcount, dcount
    try:
        connection.mkd(remotedir)
        print remotedir, 'directory created'
    except: 
        print remotedir, 'directory not created'
    connection.cwd(remotedir)
    localfiles = os.listdir(localdir)
    for localname in localfiles:  
        localpath = os.path.join(localdir, localname) 
        print 'uploading', localpath, 'to', localname
        if os.path.isdir(localpath):
            # recur into subdirs
            uploadDir(localpath, localname, connection)
            connection.cwd('..')
            dcount = dcount+1
        else:
            if localname[-4:] == 'html' or localname[-3:] == 'txt':
                # use ascii mode xfer
                localfile = open(localpath, 'r')
                connection.storlines('STOR ' + localname, localfile)
            else:
                # use binary mode xfer
                localfile = open(localpath, 'rb')
                connection.storbinary('STOR ' + localname, localfile, 1024)
            localfile.close()
            fcount = fcount+1

if __name__ == '__main__':
    remotesite   = 'home.rmi.net'         # upload to rmi.net
    topremotedir = 'public_html'
    remoteuser   = 'lutz'
    remotepass   = getpass('Please enter password for %s: ' % remotesite)
    toplocaldir  = (len(sys.argv) > 1 and sys.argv[1]) or '.'

    print 'connecting...'
    connection = ftplib.FTP(remotesite)               # connect to ftp site
    connection.login(remoteuser, remotepass)          # login as user/password
    fcount = dcount = 0
    uploadDir(toplocaldir, topremotedir, connection)
    connection.quit()
    print 'Done:', fcount, 'files and', dcount, 'directories uploaded.'
