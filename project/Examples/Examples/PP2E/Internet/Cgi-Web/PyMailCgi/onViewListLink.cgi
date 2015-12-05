#!/usr/bin/python
############################################################
# On user click of message link in main selection list;
# cgi.FieldStorage undoes any urllib escapes in the link's
# input parameters (%xx and '+' for spaces already undone);
############################################################

import cgi, rfc822, StringIO
import commonhtml, loadmail
from secret import decode
#commonhtml.dumpstatepage(0)

form = cgi.FieldStorage()
user, pswd, site = commonhtml.getstandardpopfields(form)
try:
    msgnum   = form['mnum'].value                               # from url link
    newmail  = loadmail.loadnewmail(site, user, decode(pswd))
    textfile = StringIO.StringIO(newmail[int(msgnum) - 1])      # don't eval!
    headers  = rfc822.Message(textfile)
    bodytext = textfile.read()
    commonhtml.viewpage(msgnum, headers, bodytext, form)        # encoded pswd
except: 
    commonhtml.errorpage('Error loading message')
