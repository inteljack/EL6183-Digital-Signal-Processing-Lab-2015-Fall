#########################################################
# on submit request: store or mail data, send reply page;
# report data is stored in dictionaries on the database;
# we require a description field (and return a page with
# an error message if it's empty), even though the dbase
# mechanism could handle empty description fields--it 
# makes no sense to submit a bug without a description;
#########################################################

import cgi, os, sys, string
mailto = 'lutz@rmi.net'             # or lutz@starship.python.net
sys.stderr = sys.stdout             # print errors to browser
print "Content-type: text/html\n"

thankyouHtml = """
<TITLE>Thank you</TITLE>
<H1>Thank you</H1> 
<P>%s</P>
<HR>"""

errorHtml = """
<TITLE>Empty field</TITLE>
<H1>Error: Empty %s</H1> 
<P>Sorry, you forgot to provide a '%s' value.
Please go back to the prior page and try again.</P>
<HR>"""

def sendMail(inputs):                             # email data to author
    text = ''                                     # or 'mailto:' form action
    for key, val in inputs.items():               # or smtplib.py or sendmail
        if val != '':
            text = text + ('%s = %s\n' % (key, val))
    mailcmd = 'mail -s "PP2E Errata" %s' % mailto
    os.popen(mailcmd, 'w').write(text)

def saveAndReply(dbase, inputs, replyStored, replyMailed):
    form = cgi.FieldStorage()
    for key in form.keys():
        if key in inputs.keys():
            inputs[key] = form[key].value       # pick out entered fields

    required = ['Description']
    for field in required:
        if string.strip(inputs[field]) == '':
            print errorHtml % (field, field)    # send error page to browser
            break
    else:
        if inputs['Submit mode'] == 'email':
            sendMail(inputs)                    # email data direct to author
            print thankyouHtml % replyMailed
        else:
            dbase().storeItem(inputs)           # store data in file on server 
            print thankyouHtml % replyStored

