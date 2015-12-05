from PP2E.launchmodes import QuietPortableLauncher
def start(cmdline): QuietPortableLauncher(cmdline, cmdline)()

# start('thread-server.py')   # if not yet started

import sys
for c in 'spamSPAM':
    sys.argv = ['echo-client.py', c]
    execfile('echo-client.py')        # output appear in this window on dos
                                      # but waits for each client to finish

