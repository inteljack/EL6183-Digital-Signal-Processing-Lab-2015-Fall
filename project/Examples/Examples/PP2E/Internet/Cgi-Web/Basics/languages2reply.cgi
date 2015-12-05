#!/usr/bin/python
#########################################################
# for easier maintenance, use html template strings, get
# the language table and input key from common mdule file,
# and get reusable form field mockup utilities module.
#########################################################

import cgi, sys
from formMockup import FieldMockup                   # input field simulator
from languages2common import hellos, inputkey        # get common table, name
debugme = 0

hdrhtml = """Content-type: text/html\n
<TITLE>Languages</TITLE>
<H1>Syntax</H1><HR>"""
 
langhtml = """
<H3>%s</H3><P><PRE>
%s
</PRE></P><BR>"""

def showHello(form):                                 # html for one language
    choice = form[inputkey].value                    # escape lang name too
    try:
        print langhtml % (cgi.escape(choice),
                          cgi.escape(hellos[choice]))
    except KeyError:
        print langhtml % (cgi.escape(choice), 
                         "Sorry--I don't know that language")

def main():
    if debugme:
        form = {inputkey: FieldMockup(sys.argv[1])}  # name on cmd line
    else:
        form = cgi.FieldStorage()                    # parse real inputs
    
    print hdrhtml
    if not form.has_key(inputkey) or form[inputkey].value == 'All':
        for lang in hellos.keys():
            mock = {inputkey: FieldMockup(lang)}
            showHello(mock)
    else:
        showHello(form)
    print '<HR>' 

if __name__ == '__main__': main()
