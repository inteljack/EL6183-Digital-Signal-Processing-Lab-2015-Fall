#!/usr/bin/python
# On submit in pop password input window--make view list

import cgi, StringIO, rfc822, string
import loadmail, commonhtml 
from   secret import encode        # user-defined encoder module
MaxHdr = 35                        # max length of email hdrs in list

# only pswd comes from page here, rest usually in module
formdata = cgi.FieldStorage()
mailuser, mailpswd, mailsite = commonhtml.getstandardpopfields(formdata)

try:
    newmail  = loadmail.loadnewmail(mailsite, mailuser, mailpswd)
    mailnum  = 1
    maillist = []
    for mail in newmail:
        msginfo = []
        hdrs = rfc822.Message(StringIO.StringIO(mail))
        for key in ('Subject', 'From', 'Date'):
            msginfo.append(hdrs.get(key, '?')[:MaxHdr])
        msginfo = string.join(msginfo, ' | ')
        maillist.append((msginfo, commonhtml.urlroot + '/onViewListLink.cgi', 
                                      {'mnum': mailnum,
                                       'user': mailuser,          # data params
                                       'pswd': encode(mailpswd),  # pass in url
                                       'site': mailsite}))        # not inputs
        mailnum = mailnum+1
    commonhtml.listpage(maillist, 'mail selection list')
except:
    commonhtml.errorpage('Error loading mail index')
