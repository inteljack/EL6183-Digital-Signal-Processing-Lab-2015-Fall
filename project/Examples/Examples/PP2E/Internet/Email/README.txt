Scripts popmail.py and smtpmail.py retrieve mail
from a POP email server, and send a new mail to 
a SMTP email server, respectively.  They work on 
any machine with sockets (even Windows--your machine
will automaically dial out to your ISP when these
scripts run, if needed), but you will want to 
change the server names in file "mailconfig.py"
to be servers on which you have an email account.

Script pymail.py is a simple interactive email 
client which browses a pop email account, and 
sends to a smpt email account (via smptmail.py).
PyMailGui.py adds a Tkinter interface to pop/smtp
email processing; see also PyMailCgi in the Cgi
section, which adds a browser-based interface.

Other scripts to decode email attachments, which I 
wrote to handle complex emails from a command-line
interface:

decode64.py
    uses the base64 module to decode a file of 
    base64 encoded text; assumes you have extracted
    such text from a mail message already; uudecoding
    works similarly (module uu)

decode64_b.py
    same, but uses the mimetools.decode utility,
    instead of the base64 module

decodeAll.py
    reads an entire email message and decodes and
    saves its body parts in individual files; handles
    multipart messages, base64 and uu encoded attachments,
    and more; names files intelligently if no filename is
    given; uses the mhlib module, which uses mimetools and 
    multifile modules;  reads/parses rfc mail headers and
    attachment separators, so you don't need to extract
    parts manually first

There are many additional email (and other Internet 
protocol) tools in the Python standard source library, 
including higher-level mailbox handlers, and parallel
tools for encoding (rather than decoding) attachments.
See the Library Manual for more details.

See also: the unix mail file processing logic in
the application framework examples atthe end of 
the languages section.
