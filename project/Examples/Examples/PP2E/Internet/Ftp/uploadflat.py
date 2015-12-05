#!/bin/env python 
##########################################################################
# use ftp to upload all files from a local dir to a remote site/directory;
# e.g., run me to copy a web/ftp site's files from your PC to your ISP;
# assumes a flat directory upload: uploadall.py does nested directories.
# to go to my ISP, I change setting to 'home.rmi.net', and 'public_html'.
##########################################################################

import os, sys, ftplib, getpass

remotesite = 'starship.python.net'                  # upload to starship site
remotedir  = 'public_html/home'                     # from win laptop or other
remoteuser = 'lutz'
remotepass = getpass.getpass('Please enter password for %s: ' % remotesite)
localdir   = (len(sys.argv) > 1 and sys.argv[1]) or '.'
if sys.platform[:3] == 'win': raw_input()           # clear stream
cleanall   = raw_input('Clean remote directory first? ')[:1] in ['y', 'Y']

print 'connecting...'
connection = ftplib.FTP(remotesite)                 # connect to ftp site
connection.login(remoteuser, remotepass)            # login as user/password
connection.cwd(remotedir)                           # cd to directory to copy

if cleanall:
    for remotename in connection.nlst():            # try to delete all remotes
        try:                                        # first to remove old files
            print 'deleting remote', remotename
            connection.delete(remotename)           
        except:                                     
            print 'cannot delete remote', remotename

count = 0
localfiles = os.listdir(localdir)                   # upload all local files
                                                    # listdir() strips dir path
for localname in localfiles:  
    localpath = os.path.join(localdir, localname) 
    print 'uploading', localpath, 'to', localname
    if localname[-4:] == 'html' or localname[-3:] == 'txt':
        # use ascii mode xfer
        localfile = open(localpath, 'r')
        connection.storlines('STOR ' + localname, localfile)
    else:
        # use binary mode xfer
        localfile = open(localpath, 'rb')
        connection.storbinary('STOR ' + localname, localfile, 1024)
    localfile.close()
    count = count+1

connection.quit()
print 'Done:', count, 'files uploaded.'
