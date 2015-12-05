#!/usr/bin/python
#######################################################
# runs on the server, reads form input, prints html;
# url http://server-name/root-dir/Basics/test4.cgi
#######################################################

import cgi, sys
sys.stderr = sys.stdout              # errors to browser
form = cgi.FieldStorage()            # parse form data
print "Content-type: text/html\n"    # plus blank line

# class dummy:
#     def __init__(self, s): self.value = s
# form = {'user': dummy('bob'), 'age':dummy('10')}

html = """
<TITLE>test4.cgi</TITLE>
<H1>Greetings</H1>
<HR>
<H4>%s</H4>
<H4>%s</H4>
<H4>%s</H4>
<HR>"""

if not form.has_key('user'):
    line1 = "Who are you?"
else:
    line1 = "Hello, %s." % form['user'].value

line2 = "You're talking to a %s server." % sys.platform

line3 = ""
if form.has_key('age'):
    try:
        line3 = "Your age squared is %d!" % (int(form['age'].value) ** 2)
    except:
        line3 = "Sorry, I can't compute %s ** 2." % form['age'].value

print html % (line1, line2, line3)

