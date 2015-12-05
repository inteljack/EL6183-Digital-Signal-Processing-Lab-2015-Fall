#!/usr/bin/python
#################################################################
# Display languages.cgi script code without running it.
#################################################################

import cgi
filename = 'languages.cgi'

print "Content-type: text/html\n"       # wrap up in html
print "<TITLE>Languages</TITLE>"
print "<H1>Source code: '%s'</H1>" % filename
print '<HR><PRE>' 
print cgi.escape(open(filename).read())
print '</PRE><HR>' 
