#!/usr/bin/python
# On submit in mail view window, action selected=(fwd, reply, delete)

import cgi, string
import commonhtml, secret
from   externs import pymail, mailconfig
from   commonhtml import getfield

def quotetext(form):
    """
    note that headers come from the prior page's form here,
    not from parsing the mail message again; that means that 
    commonhtml.viewpage must pass along date as a hidden field
    """ 
    quoted = '\n-----Original Message-----\n'
    for hdr in ('From', 'To', 'Date'):
        quoted = quoted + '%s: %s\n' % (hdr, getfield(form, hdr))
    quoted = quoted + '\n' +   getfield(form, 'text')
    quoted = '\n' + string.replace(quoted, '\n', '\n> ')
    return quoted

form = cgi.FieldStorage()  # parse form or url data
user, pswd, site = commonhtml.getstandardpopfields(form)

try:
    if form['action'].value   == 'Reply':
        headers = {'From':    mailconfig.myaddress,
                   'To':      getfield(form, 'From'),
                   'Cc':      mailconfig.myaddress,
                   'Subject': 'Re: ' + getfield(form, 'Subject')}
        commonhtml.editpage('Reply', headers, quotetext(form))

    elif form['action'].value == 'Forward':
        headers = {'From':    mailconfig.myaddress,
                   'To':      '',
                   'Cc':      mailconfig.myaddress,
                   'Subject': 'Fwd: ' + getfield(form, 'Subject')}
        commonhtml.editpage('Forward', headers, quotetext(form))

    elif form['action'].value == 'Delete':
        msgnum = int(form['mnum'].value)       # or string.atoi, but not eval()
        commonhtml.runsilent(                  # mnum field is required here
            pymail.deletemessages,
                (site, user, secret.decode(pswd), [msgnum], 0) )
        commonhtml.confirmationpage('Delete')

    else:
       assert 0, 'Invalid view action requested'
except:
    commonhtml.errorpage('Cannot process view action')
