#!/usr/bin/python
# On submit in edit window--finish a write, reply, or forward

import cgi, smtplib, time, string, commonhtml
#commonhtml.dumpstatepage(0)
form = cgi.FieldStorage()                      # parse form input data

# server name from module or get-style url
smtpservername = commonhtml.getstandardsmtpfields(form)

# parms assumed to be in form or url here
from commonhtml import getfield                # fetch value attributes
From = getfield(form, 'From')                  # empty fields may not be sent
To   = getfield(form, 'To')
Cc   = getfield(form, 'Cc')
Subj = getfield(form, 'Subject')
text = getfield(form, 'text')

# caveat: logic borrowed from PyMailGui
date  = time.ctime(time.time())
Cchdr = (Cc and 'Cc: %s\n' % Cc) or ''
hdrs  = ('From: %s\nTo: %s\n%sDate: %s\nSubject: %s\n' 
                 % (From, To, Cchdr, date, Subj))
hdrs  = hdrs + 'X-Mailer: PyMailCgi Version 1.0 (Python)\n'

Ccs = (Cc and string.split(Cc, ';')) or []     # some servers reject ['']
Tos = string.split(To, ';') + Ccs              # cc: hdr line, and To list
Tos = map(string.strip, Tos)                   # some addrs can have ','s

try:                                              # smtplib may raise except
    server = smtplib.SMTP(smtpservername)         # or return failed Tos dict
    failed = server.sendmail(From, Tos, hdrs + text)
    server.quit()
except:
    commonhtml.errorpage('Send mail error')
else:
    if failed:
        errInfo = 'Send mail error\nFailed recipients:\n' + str(failed)
        commonhtml.errorpage(errInfo)
    else:
        commonhtml.confirmationpage('Send mail')
