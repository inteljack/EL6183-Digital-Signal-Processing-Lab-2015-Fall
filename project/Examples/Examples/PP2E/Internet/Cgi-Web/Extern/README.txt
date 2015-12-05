When I copy the Cgi-Web directory to a server machine,
I also put a few utility modules in this directory, 
copied over from the PP2E.Internet.Email package.
See PyMailCgi/externs.py for more details.  

This is only needed because I'm selective about which
book example dirs are installed on the web server.  I 
install only the Cgi-Web directory here in my public_html 
directory on the server machine; there is no PP2E root 
directory on the server.

Note: this directory/package is called Extern; it is not
the same as module PyMailCgi/externs.py (which imports 
from package Extern).
