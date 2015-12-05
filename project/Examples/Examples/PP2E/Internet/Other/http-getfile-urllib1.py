###################################################################
# fetch a file from an http (web) server over sockets via urllib;
# urllib supports http, ftp, files, etc. via url address strings;
# for hhtp, the url can name a file or trigger a remote cgi script;
# see also the urllib example in the ftp section, and the cgi 
# script invocation in a later chapter; files can be fetched over
# the net with Python in many ways that vary in complexity and 
# server requirements: sockets, ftp, http, urllib, cgi outputs;
# caveat: should run urllib.quote on filename--see later chapters;
###################################################################

import sys, urllib
showlines = 6
try:
    servername, filename = sys.argv[1:]              # cmdline args?
except:
    servername, filename = 'starship.python.net', '/index.html'

remoteaddr = 'http://%s%s' % (servername, filename)  # can name a cgi script too
print remoteaddr
remotefile = urllib.urlopen(remoteaddr)              # returns input file object
remotedata = remotefile.readlines()                  # read data directly here
remotefile.close()
for line in remotedata[:showlines]: print line,
