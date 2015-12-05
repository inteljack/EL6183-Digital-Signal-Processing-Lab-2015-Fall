############################################
# email scripts get server names from here:
# change to reflect your machine/user names;
# could get these in command line instead
############################################

# SMTP email server machine (send)
smtpservername = 'smtp.rmi.net'          # or starship.python.net, 'localhost'

# POP3 email server machine, user (retrieve)
popservername  = '?your-pop-server?'     # or starship.python.net, 'localhost'
popusername    = '?your-pop-name?'       # password is requested when run

# local file where pymail (not PyMailGui) saves pop mail
savemailfile   = r'c:\temp\savemail.txt'

# personal info used by PyMailGui to fill in forms;
# sig-- can be a triple-quoted block, ignored if empty string;
# addr--used for initial value of "From" field if not empty,
# else tries to guess From for replies, with varying success;

myaddress   = '?your-email-address?'
mysignature = '--Your Name  (http://your-home-page)  [PyMailCgi 1.0]'
