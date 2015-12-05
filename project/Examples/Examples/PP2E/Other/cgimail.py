#!/usr/local/bin/python

import os, string, sys
from cgi import *

# The trailing space is required!
sendmail_cmd = "/usr/lib/sendmail -oi "


def SendError(str):
    errmsg = escape(str)
    print "Content-type: text/html\n\n"
    print "<HEADER>\n<TITLE> CGI Error </TITLE>\n</HEADER>\n"
    print "<BODY>\n"
    print "<H1>CGI Error</H1>\n"
    print "<H3><STRONG>" + errmsg + "</STRONG></H3>\n"
    print "</BODY>"
    sys.exit(0)


def ShowMailForm(to):
    recipient = escape(to)
    title = "Mail to " + recipient
    print "Content-type: text/html\n\n"
    print "<HEADER>\n<TITLE>" + title + "</TITLE>\n</HEADER>\n"
    print "<BODY>\n"
    print "<H1>" + title + "</H1>\n"
    print '<FORM ACTION="/cgi-bin/cgimail" METHOD=POST>'
    print '<INPUT TYPE="hidden" NAME="to" VALUE="' + recipient + '"> <P>'
    print '<P ALIGN=center><TABLE BORDER CELLPADDING=2>'
    print '<TR><TD>Your Email:</TD><TD><INPUT name="from" size=40></TD>'
    print '<TR><TD>Subject:</TD><TD><INPUT name="subj" size=40></TD>'
    print '</TABLE></P>'
    print '<P><TEXTAREA name="msg" ROWS=12 COLS=48>Your Comments'
    print '</TEXTAREA> </P>'
    print '<P><INPUT TYPE="submit" VALUE="Submit Form"> or'
    print '<INPUT TYPE="reset"  VALUE="Reset Form"> </P>'
    print "</FORM>"
    #print_environ()
    print "</BODY>"


def SendMail():
    form = FormContent()    # handles stdin parsing

    # Required Items
    if not form.has_key("to"):   SendError("No Recipient Specified")
    if not form.has_key("from"): SendError("No Sender Specified")
    if not form.has_key("msg"):  SendError("No Message Specified")
    real_to   = form["to"][0]
    real_from = form["from"][0]
    real_msg  = form["msg"][0]

    # Non-required Items
    real_name = "UNKNOWN SENDER"
    real_subj = ""
    if form.has_key("name"): real_name = form["name"][0]
    if form.has_key("subj"): real_subj = form["subj"][0]

    # Send the mail.
    try: mfd = os.popen(sendmail_cmd + real_to, "w")
    except: SendError("Unable to send mail")
    
    mfd.write("To:   " + real_to + "\n")
    mfd.write("From: " + real_from + "\n")
    mfd.write("Subject:  " + real_subj + "\n")
    mfd.write("X-Sender: " + real_name + "\n")
    mfd.write("X-Warning: This mail was sent from an HTTPD server. No\n")
    mfd.write("X-Warning: attempt was made to verify the sender's identity.\n")
    mfd.write("\n" + real_msg + "\n")
    mfd.close()    

    # Output Resulting HTML page.
    # When writing HTML, we must be careful to escape any special
    # characters.  The escape() routine handles the translation
    # for us.
    #
    real_to   = escape( real_to )
    real_from = escape( real_from )
    real_name = escape( real_name )
    real_msg  = escape( real_msg )

    print "Content-type: text/html\n\n"
    print "<HEADER>\n<TITLE> Mail Sent to " + real_to + "</TITLE>\n</HEADER>\n"
    print "<BODY>\n"
    print "<H1>Successfully sent mail to " + real_to + "</H1>\n"
    print "Here's what was sent:<P><HR><PRE>"
    print "To:   " + real_to
    print "From: " + real_from
    print "Subject: " + real_subj
    print "X-Sender: " + real_name
    print "X-Warning: This mail was sent from an HTTPD server. No"
    print "X-Warning: attempt was made to verify the sender's identity."
    print "\n" + real_msg
    print "</PRE><HR>"
    print "</BODY>"


def Main():
    if len(sys.argv) == 1:
        SendMail()
    elif len(sys.argv) == 2:
        ShowMailForm(sys.argv[1])
    else:
        SendError("Too Many Arguments on Command Line")

Main()
