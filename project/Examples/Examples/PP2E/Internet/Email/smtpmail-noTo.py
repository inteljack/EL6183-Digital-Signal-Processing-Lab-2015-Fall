#!/usr/local/bin/python
######################################################
# use the Python SMTP mail interface module to send
# email messages; this is just a simple one-shot 
# send script--see pymail, PyMailGui, and PyMailCgi
# for clients with more user interaction features, 
# and popmail.py for a script which retrieves mail; 
######################################################

import smtplib, string, sys, time, mailconfig
mailserver = mailconfig.smtpservername         # ex: starship.python.net

From = string.strip(raw_input('From? '))       # ex: lutz@rmi.net
To   = string.strip(raw_input('To?   '))       # ex: python-list@python.org
To   = string.split(To, ';')                   # allow a list of recipients
Subj = string.strip(raw_input('Subj? '))

# prepend standard headers
date = time.ctime(time.time())
text = ('From: %s\nDate: %s\nSubject: %s\n' 
                         % (From, date, Subj))

print 'Type message text, end with line=(ctrl + D or Z)'
while 1:
    line = sys.stdin.readline()
    if not line: 
        break                        # exit on ctrl-d/z
  # if line[:4] == 'From':
  #     line = '>' + line            # servers escape for us
    text = text + line

if sys.platform[:3] == 'win': print
print 'Connecting...'
server = smtplib.SMTP(mailserver)              # connect, no login step
failed = server.sendmail(From, To, text)
server.quit() 
if failed:                                     # smtplib may raise exceptions
    print 'Failed recipients:', failed         # too, but let them pass here
else:
    print 'No errors.'
print 'Bye.'

