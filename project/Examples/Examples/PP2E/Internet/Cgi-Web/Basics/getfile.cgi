#!/usr/bin/python
#################################################################
# Display any cgi (or other) server-side file without running it.
# The file name can be passed in a URL param or form field; e.g.,
# http://server/~lutz/Basics/getfile.cgi?filename=somefile.cgi.
# Users can cut-and-paste or "View source" to save file locally.
# On IE, running the text/plain version (formatted=0) sometimes
# pops up Notepad, but end-of-lines are not always in DOS format; 
# Netscape shows the text correctly in the browser page instead.
# Sending the file in text/html mode works on both browsers--text
# is displayed in the browser response page correctly. We also 
# check the filename here to try to avoid showing private files;
# this may or may not prevent access to such files in general.
#################################################################

import cgi, os, sys
formatted = 1                                  # 1=wrap text in html
privates  = ['../PyMailCgi/secret.py']         # don't show these

html = """
<html><title>Getfile response</title>
<h1>Source code for: '%s'</h1>
<hr>
<pre>%s</pre>
<hr></html>"""

def restricted(filename):
    for path in privates:
        if os.path.samefile(path, filename):   # unify all paths by os.stat
            return 1                           # else returns None=false
 
try:
    form = cgi.FieldStorage()
    filename = form['filename'].value          # url param or form field
except:
    filename = 'getfile.cgi'                   # else default filename

try:
    assert not restricted(filename)            # load unless private
    filetext = open(filename).read()
except AssertionError:
    filetext = '(File access denied)'
except:
    filetext = '(Error opening file: %s)' % sys.exc_value

if not formatted:
    print "Content-type: text/plain\n"         # send plain text
    print filetext                             # works on NS, not IE
else:
    print "Content-type: text/html\n"          # wrap up in html
    print html % (filename, cgi.escape(filetext))
