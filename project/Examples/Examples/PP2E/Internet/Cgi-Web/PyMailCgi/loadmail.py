###################################################################
# mail list loader; future--change me to save mail list between
# cgi script runs, to avoid reloading all mail each time; this
# won't impact clients that use the interfaces here if done well;
# for now, to keep this simple, reloads all mail on each operation
###################################################################

from commonhtml import runsilent         # suppress print's (no verbose flag)
from externs    import Email

# load all mail from number 1 up
# this may trigger an exception

def loadnewmail(mailserver, mailuser, mailpswd):
    return runsilent(Email.pymail.loadmessages,
                                  (mailserver, mailuser, mailpswd))
