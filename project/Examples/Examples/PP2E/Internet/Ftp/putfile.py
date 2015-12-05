#!/usr/local/bin/python
################################################## 
# Store an arbitrary file by ftp.  Anonymous 
# ftp unless you pass a user=(name, pswd) tuple.
##################################################
 
import ftplib                    # socket-based ftp tools

file = 'sousa.au'                # default file coordinates
site = 'starship.python.net'     # monty python theme song
dir  = 'upload'

def putfile(file=file, site=site, dir=dir, user=(), verbose=1):
    """
    store a file by ftp to a site/directory
    anonymous or real login, binary transfer
    """
    if verbose: print 'Uploading', file
    local  = open(file, 'rb')               # local file of same name
    remote = ftplib.FTP(site)               # connect to ftp site
    apply(remote.login, user)               # anonymous or real login
    remote.cwd(dir)
    remote.storbinary('STOR ' + file, local, 1024)
    remote.quit()
    local.close()
    if verbose: print 'Upload done.'

if __name__ == '__main__':
    import sys, getpass
    pswd = getpass.getpass(site + ' pswd?')          # filename on cmdline
    putfile(file=sys.argv[1], user=('lutz', pswd))   # non-anonymous login
