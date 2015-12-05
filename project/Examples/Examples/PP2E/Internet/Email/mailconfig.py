################################################################
# email scripts get their server names and other email config
# options from this module: change me to reflect your machine
# names, sig, etc.; could get some from the command line too;
################################################################

#-------------------------------------------
# SMTP email server machine name (send)
#-------------------------------------------

smtpservername = 'smtp.rmi.net'          # or starship.python.net, 'localhost'

#-------------------------------------------
# POP3 email server machine, user (retrieve)
#-------------------------------------------

popservername  = '?your server name?'    # or starship.python.net, 'localhost'
popusername    = '?your user name?'      # password fetched or asked when run

#-------------------------------------------
# local file where pymail saves pop mail
# PyMailGui insead asks with a popup dialog
#-------------------------------------------

savemailfile   = r'c:\temp\savemail.txt'       # use dialog in PyMailGui

#---------------------------------------------------------------
# PyMailGui: optional name of local one-line text file with your 
# pop password; if empty or file cannot be read, pswd requested 
# when run; pswd is not encrypted so leave this empty on shared 
# machines; PyMailCgi and pymail always ask for pswd when run.
#---------------------------------------------------------------

poppasswdfile  = r'c:\temp\pymailgui.txt'      # set to '' to be asked

#---------------------------------------------------------------
# personal information used by PyMailGui to fill in forms;
# sig  -- can be a triple-quoted block, ignored if empty string;
# addr -- used for initial value of "From" field if not empty,
# else tries to guess From for replies, with varying success;
#---------------------------------------------------------------

myaddress   = '?your email address?'
mysignature = '?your email signature line?  [PyMailGui 1.0]'
