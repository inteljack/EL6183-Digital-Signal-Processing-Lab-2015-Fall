##############################################################
# Isolate all imports of modules that live outside of the
# PyMailCgi PyMailCgi directory.  Normally, these would come
# from PP2E.Internet.Email, but when I install PyMailCgi, 
# I copy just the Cgi-Web directory's contents to public_html
# on the server, so there is no PP2E directory on the server.
# Instead, I either copy the imports referenced in this file to 
# the PyMailCgi parent directory, or tweak the dir appended to
# the sys.path module search path here.  Because all other 
# modules get the externals from here, there is only one place
# to change when they are relocated.  This may be arguably
# gross, but I only put Internet code on the server machine.
##############################################################

import sys
sys.path.append('..')                 # see dir where Email installed on server
from  Extern import Email             # assumes a ../Extern dir with Email dir
from  Extern.Email import pymail      # can use names Email.pymail or pymail
from  Extern.Email import mailconfig
