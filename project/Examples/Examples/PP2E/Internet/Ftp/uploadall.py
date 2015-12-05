#!/bin/env python
##########################################################################
# use ftp to upload all files from a local dir to a remote site/directory;
# this version supports uploading nested subdirectories too, but not the 
# cleanall option (that requires parsing ftp listings to detect remote 
# dirs, etc.);  to upload subdirectories, uses os.path.isdir(path) to see 
# if a local file is really a directory, FTP().mkd(path) to make the dir
# on the remote machine (wrapped in a try in case it already exists there), 
# and recursion to upload all files/dirs inside the nested subdirectory. 
# see also: uploadall-2.py, which doesn't assume the topremotedir exists.
##########################################################################
  
import os, sys, ftplib
from getpass import getpass

remotesite   = 'home.rmi.net'          # upload from pc or starship to rmi.net
topremotedir = 'public_html' 
remoteuser   = 'lutz'
remotepass   = getpass('Please enter password for %s: ' % remotesite)
toplocaldir  = (len(sys.argv) > 1 and sys.argv[1]) or '.'

print 'connecting...'
connection = ftplib.FTP(remotesite)               # connect to ftp site
connection.login(remoteuser, remotepass)          # login as user/password
connection.cwd(topremotedir)                      # cd to directory to copy to
                                                  # assumes topremotedir exists
def uploadDir(localdir):
    global fcount, dcount
    localfiles = os.listdir(localdir)
    for localname in localfiles:  
        localpath = os.path.join(localdir, localname) 
        print 'uploading', localpath, 'to', localname
        if os.path.isdir(localpath):
            # recur into subdirs
            try:
                connection.mkd(localname)
                print localname, 'directory created'
            except: 
                print localname, 'directory not created'
            connection.cwd(localname)
            uploadDir(localpath)
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

fcount = dcount = 0
uploadDir(toplocaldir)
connection.quit()
print 'Done:', fcount, 'files and', dcount, 'directories uploaded.'
