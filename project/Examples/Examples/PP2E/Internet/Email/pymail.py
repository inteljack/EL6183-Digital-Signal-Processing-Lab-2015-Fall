#!/usr/local/bin/python
######################################################
# A simple command-line email interface client in 
# Python; uses Python POP3 mail interface module to
# view pop email account messages; uses rfc822 and
# StringIO modules to extract mail message headers; 
######################################################

import poplib, rfc822, string, StringIO

def connect(servername, user, passwd):
    print 'Connecting...'
    server = poplib.POP3(servername)
    server.user(user)                    # connect, login to mail server
    server.pass_(passwd)                 # pass is a reserved word
    print server.getwelcome()            # print returned greeting message 
    return server

def loadmessages(servername, user, passwd, loadfrom=1):
    server = connect(servername, user, passwd)
    try:
        print server.list()
        (msgCount, msgBytes) = server.stat()
        print 'There are', msgCount, 'mail messages in', msgBytes, 'bytes'
        print 'Retrieving:',
        msgList = []
        for i in range(loadfrom, msgCount+1):            # empty if low >= high
            print i,                                     # fetch mail now
            (hdr, message, octets) = server.retr(i)      # save text on list
            msgList.append(string.join(message, '\n'))   # leave mail on server 
        print
    finally:
        server.quit()                                    # unlock the mail box
    assert len(msgList) == (msgCount - loadfrom) + 1     # msg nums start at 1
    return msgList

def deletemessages(servername, user, passwd, toDelete, verify=1):
    print 'To be deleted:', toDelete
    if verify and raw_input('Delete?')[:1] not in ['y', 'Y']:
        print 'Delete cancelled.'
    else:
        server = connect(servername, user, passwd)
        try:
            print 'Deleting messages from server.'
            for msgnum in toDelete:                 # reconnect to delete mail
                server.dele(msgnum)                 # mbox locked until quit()
        finally:
            server.quit()

def showindex(msgList):
    count = 0   
    for msg in msgList:                      # strip,show some mail headers
        strfile = StringIO.StringIO(msg)     # make string look like a file
        msghdrs = rfc822.Message(strfile)    # parse mail headers into a dict
        count   = count + 1
        print '%d:\t%d bytes' % (count, len(msg))
        for hdr in ('From', 'Date', 'Subject'):
            try:
                print '\t%s=>%s' % (hdr, msghdrs[hdr])
            except KeyError:
                print '\t%s=>(unknown)' % hdr
            #print '\n\t%s=>%s' % (hdr, msghdrs.get(hdr, '(unknown)')
        if count % 5 == 0:
            raw_input('[Press Enter key]')  # pause after each 5 

def showmessage(i, msgList):
    if 1 <= i <= len(msgList):
        print '-'*80
        print msgList[i-1]              # this prints entire mail--hdrs+text
        print '-'*80                    # to get text only, call file.read()
    else:                               # after rfc822.Message reads hdr lines
        print 'Bad message number'

def savemessage(i, mailfile, msgList):
    if 1 <= i <= len(msgList):
        open(mailfile, 'a').write('\n' + msgList[i-1] + '-'*80 + '\n')
    else:
        print 'Bad message number'

def msgnum(command):
    try:
        return string.atoi(string.split(command)[1])
    except:
        return -1   # assume this is bad

helptext = """
Available commands:
i     - index display
l n?  - list all messages (or just message n)
d n?  - mark all messages for deletion (or just message n)
s n?  - save all messages to a file (or just message n)
m     - compose and send a new mail message
q     - quit pymail
?     - display this help text
"""

def interact(msgList, mailfile):
    showindex(msgList)
    toDelete = []
    while 1:
        try:
            command = raw_input('[Pymail] Action? (i, l, d, s, m, q, ?) ')
        except EOFError:
            command = 'q'

        # quit
        if not command or command == 'q': 
            break

        # index
        elif command[0] == 'i':          
            showindex(msgList)

        # list
        elif command[0] == 'l':         
            if len(command) == 1:
                for i in range(1, len(msgList)+1): 
                    showmessage(i, msgList)
            else:
                showmessage(msgnum(command), msgList)

        # save
        elif command[0] == 's':        
            if len(command) == 1:
                for i in range(1, len(msgList)+1): 
                    savemessage(i, mailfile, msgList)
            else:
                savemessage(msgnum(command), mailfile, msgList)

        # delete 
        elif command[0] == 'd':               
            if len(command) == 1:
                toDelete = range(1, len(msgList)+1)     # delete all later
            else:
                delnum = msgnum(command)
                if (1 <= delnum <= len(msgList)) and (delnum not in toDelete):
                    toDelete.append(delnum)
                else:
                    print 'Bad message number'

        # mail
        elif command[0] == 'm':                # send a new mail via smtp
            try:                               # reuse existing script
                execfile('smtpmail.py', {})    # run file in own namespace
            except:
                print 'Error - mail not sent'  # don't die if script dies

        elif command[0] == '?':
            print helptext
        else:
            print 'What? -- type "?" for commands help'
    return toDelete

if __name__ == '__main__':
    import sys, getpass, mailconfig
    mailserver = mailconfig.popservername        # ex: 'starship.python.net'
    mailuser   = mailconfig.popusername          # ex: 'lutz'
    mailfile   = mailconfig.savemailfile         # ex:  r'c:\stuff\savemail'
    mailpswd   = getpass.getpass('Password for %s?' % mailserver)

    if sys.platform[:3] == 'win': raw_input()    # clear stream
    print '[Pymail email client]'
    msgList    = loadmessages(mailserver, mailuser, mailpswd)     # load all
    toDelete   = interact(msgList, mailfile)
    if toDelete: deletemessages(mailserver, mailuser, mailpswd, toDelete)
    print 'Bye.'
