####################################################################
# fetch a file from an http (web) server over sockets via urlllib;
# this version uses an interface that saves the fetched data to a
# local file; the local file name is either passed in as a cmdline 
# arg or stripped from the url with urlparse: the filename argument
# may have a directory path at the front and query parmams at end,
# so os.path.split is not enough (only splits off directory path);  
# caveat: should run urllib.quote on filename--see later chapters;
####################################################################

import sys, os, urllib, urlparse
showlines = 6
try:
    servername, filename = sys.argv[1:3]              # first 2 cmdline args?
except:
    servername, filename = 'starship.python.net', '/index.html'

remoteaddr = 'http://%s%s' % (servername, filename)   # any address on the net
if len(sys.argv) == 4:                                # get result file name
    localname = sys.argv[3]
else:
    (scheme, server, path, parms, query, frag) = urlparse.urlparse(remoteaddr)
    localname = os.path.split(path)[1]

print remoteaddr, localname
urllib.urlretrieve(remoteaddr, localname)               # can be file or script
remotedata = open(localname).readlines()                # saved to local file
for line in remotedata[:showlines]: print line,
