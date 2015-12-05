#!/usr/local/bin/python
######################################################
# use the Python POP3 mail interface module to view
# your pop email account messages; this is just a 
# simple listing--see pymail.py for a client with
# more user interaction features, and smtpmail.py 
# for a script which sends mail; pop is used to 
# retrieve mail, and runs on a socket using port 
# number 110 on the server machine, but Python's 
# poplib hides all protocol details; to send mail, 
# use the smtplib module (or os.popen('mail...').
# see also: unix mailfile reader in App framework.
######################################################

import poplib, getpass, sys, mailconfig

mailserver = mailconfig.popservername      # ex: 'pop.rmi.net'
mailuser   = mailconfig.popusername        # ex: 'lutz'
mailpasswd = getpass.getpass('Password for %s?' % mailserver)

print 'Connecting...'
server = poplib.POP3(mailserver)
server.user(mailuser)                      # connect, login to mail server
server.pass_(mailpasswd)                   # pass is a reserved word

try:
    print server.getwelcome()              # print returned greeting message 
    msgCount, msgBytes = server.stat()
    print 'There are', msgCount, 'mail messages in', msgBytes, 'bytes'
    print server.list()
    print '-'*80
    if sys.platform[:3] == 'win': raw_input()      # windows getpass is odd
    raw_input('[Press Enter key]')

    for i in range(msgCount):
        hdr, message, octets = server.retr(i+1)    # octets is byte count
        for line in message: print line            # retrieve, print all mail
        print '-'*80                               # mail box locked till quit
        if i < msgCount - 1: 
           raw_input('[Press Enter key]')
finally:                                           # make sure we unlock mbox
    server.quit()                                  # else locked till timeout
print 'Bye.'

