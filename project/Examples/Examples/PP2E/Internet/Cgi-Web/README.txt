This directory contains CGI-based book examples.  Its contents
are directly copied into the 'public_html' directory on the web
server machine used to develop the browser-based book examples.
public_html is my home directory, accessible at:

   http://starship.python.net/~lutz

besides the contents of this Cgi-Web directory, it also contains
a few non-book items (a home page mirror, plus a training CD sample).  
Non-browser Internet examples (e.g., FTP and email) are not installed
in the web derver machine, since most require a command-line interface;
try running these on your own machine or server account.

Components here:

1) Basic CGI examples
The files in the Basics subdirectory represent basic 
browser-based and/or CGI script examples.

2) PyErrata site case study
The PyErrata subdirectory here contains a self-contained
CGI-based web site--the PyErrata error reporting example
presented as a case study in the text.

3) PyMailCgi site example
The PyMailCgi subdirectory is a simple pop/smtp email 
interface implemented with cgi scripts that generate 
HTML pages (a variation and reuse of the PyMailGui 
Tk-based client system in the PP2E.Internet.Email dir).

Some of the programs in this directory can be run as is,
but all of the browser-based examples must be opened by an
Internet browser (e.g., Internet Explorer or Netscape), and
many must be run on the server machine itself instead of 
from this local directory, if you wish to run the CGI 
scripts they start.  Point your browser to:    

   http://starship.python.net/~lutz/PyInternetDemos.html

to launch examples that run in a browser or require a program
that runs on the server machine (CGI scripts).  PyInternetDemos.html
has links to all browser-based demos.  

The program LaunchBrowser.py in the examples root dir tries to do 
this browser-startup step for you automatically (by guessing where
your browser lives), but it's not completely portable or robust; 
tweak as required.  On my Windows98 and Linux machine, the script
LaunchBrowser.py opens PyInternetDemos under Internet Explorer when
double-clicked (it defaults to netscape on Linux).  You can also 
run a 'start <page>' command via os.system on Windows (see launcher).

Additonally, the top level PyDemos and PyGadgets Python+Tk programs 
use LaunchBrowser to try and open major web pages with a browser as
well; they work if a browser can be found on your machine.

INSTALL NOTES: 
If you copy this Cgi-Web directory to a server of your own, run the
script fixcgi.py here within a find command, to convert end-lines and
make cgi's executable.  On the starship server (at least), the cgi 
scripts must be in UNIX end-of-line format, not MS-DOS end-of-line 
format, else you get premature end-of-line errors when they are invoked.
See the PyTools/fixeoln_all.py script to convert to UNIX end-of-line format
if needed, or use the simple fixcgi.py script here in concert with a Unix
find.  The CGI scripts also need to be given executable mode on UNIX 
servers; use a chmod 755 command, or run fixcgi.py here (which calls 
os.chmod(file, 0755) automatically).  Some servers let you use a '.py'
extension on Python cgi scripts; I used '.cgi' for portability here.
Also see fixsitename.py to replace "starship" server references, and
install discussion on the book.

NOTE: See the ..\Other directory for examples that appear at the 
end of the final Internet chapter (JPython, HTMLGen, Zope, etc.).

