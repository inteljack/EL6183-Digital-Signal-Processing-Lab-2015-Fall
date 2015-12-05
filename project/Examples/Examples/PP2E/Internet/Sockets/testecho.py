import sys, string
from PP2E.launchmodes import QuietPortableLauncher

numclients = 8
def start(cmdline): QuietPortableLauncher(cmdline, cmdline)()

# start('echo-server.py')              # spawn server locally if not yet started

args = string.join(sys.argv[1:], ' ')  # pass server name if running remotely
for i in range(numclients):
    start('echo-client.py %s' % args)  # spawn 8? clients to test the server
