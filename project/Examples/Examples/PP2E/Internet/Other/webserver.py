#!/usr/bin/python
############################################
# implement a HTTP server in Python which 
# knows how to run server-side CGI scripts;
# change root dir for your server machine
############################################

import os
from BaseHTTPServer import HTTPServer
from CGIHTTPServer  import CGIHTTPRequestHandler
os.chdir("/home/httpd/html")                           # run in html root dir
srvraddr = ("", 80)                                    # my hostname, portnumber
srvrobj  = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever()                                # run as perpetual demon
