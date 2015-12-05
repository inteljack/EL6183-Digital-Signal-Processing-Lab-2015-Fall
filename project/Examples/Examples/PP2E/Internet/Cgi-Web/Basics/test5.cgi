#!/usr/bin/python
#######################################################
# runs on the server, reads form input, prints html;
# url=http://server-name/root-dir/Basics/test5.cgi
#######################################################

import cgi, sys, string
form = cgi.FieldStorage()            # parse form data
print "Content-type: text/html"      # plus blank line

html = """
<TITLE>test5.cgi</TITLE>
<H1>Greetings</H1>
<HR>
<H4>Your name is %(name)s</H4>
<H4>You wear rather %(shoesize)s shoes</H4>
<H4>Your current job: %(job)s</H4>
<H4>You program in %(language)s</H4>
<H4>You also said:</H4>
<P>%(comment)s</P>
<HR>"""

data = {}
for field in ['name', 'shoesize', 'job', 'language', 'comment']:
    if not form.has_key(field):
        data[field] = '(unknown)'
    else:
        if type(form[field]) != type([]):
            data[field] = form[field].value
        else:
            values = map(lambda x: x.value, form[field])
            data[field] = string.join(values, ' and ')
print html % data

