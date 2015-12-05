#!/usr/bin/python
#######################################################
# runs on the server, prints html to create a new page;
# executable permissions, stored in ~lutz/public_html,
# url=http://starship.python.net/~lutz/Basics/test0.cgi
#######################################################

print "Content-type: text/html\n"
print "<TITLE>CGI 101</TITLE>"
print "<H1>A First CGI script</H1>"
print "<P>Hello, CGI World!</P>"

