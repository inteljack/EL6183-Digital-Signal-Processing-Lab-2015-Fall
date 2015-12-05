################################################################
# spawn ftp get and put guis no matter what dir I'm run from;
# os.getcwd is not necessarily the place this script lives;
# could also hard-code a path from $PP2EHOME, or guessLocation;
# could also do this but need the DOS popup for status messages:
# from PP2E.launchmodes import PortableLauncher
# PortableLauncher('getfilegui', '%s/getfilegui.py' % mydir)()
################################################################

import os, sys
from PP2E.Launcher import findFirst
mydir = os.path.split(findFirst(os.curdir, 'PyFtpGui.pyw'))[0]

if sys.platform[:3] == 'win':
    os.system('start %s/getfilegui.py' % mydir)
    os.system('start %s/putfilegui.py' % mydir)
else:
    os.system('python %s/getfilegui.py &' % mydir)
    os.system('python %s/putfilegui.py &' % mydir)
