#!/usr/local/bin/python
################################################# 
# Fetch an arbitrary file by ftp.  Anonymous 
# ftp unless you pass a user=(name, pswd) tuple.
# Gets the Monty Python theme song by default.
#################################################
 
from ftplib  import FTP          # socket-based ftp tools
from os.path import exists       # file existence test

file = 'sousa.au'                # default file coordinates
site = 'ftp.python.org'          # monty python theme song
dir  = 'pub/python/misc'

def getfile(file=file, site=site, dir=dir, user=(), verbose=1, force=0):
    """
    fetch a file by ftp from a site/directory
    anonymous or real login, binary transfer
    """
    if exists(file) and not force:
        if verbose: print file, 'already fetched'
    else:
        if verbose: print 'Downloading', file
        local = open(file, 'wb')                # local file of same name
        try:
            remote = FTP(site)                  # connect to ftp site
            apply(remote.login, user)           # anonymous=() or (name, pswd)
            remote.cwd(dir)
            remote.retrbinary('RETR ' + file, local.write, 1024)
            remote.quit()
        finally:
            local.close()                       # close file no matter what
        if verbose: print 'Download done.'      # caller handles exceptions

if __name__ == '__main__': getfile()            # anonymous python.org login
