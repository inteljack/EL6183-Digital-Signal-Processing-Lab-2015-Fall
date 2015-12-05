# starts programs until you type 'q'

import os

parm = 0
while 1:
    parm = parm+1
    pid = os.fork()
    if pid == 0:                                             # copy process
        os.execlp('python', 'python', 'child.py', str(parm)) # overlay program
        assert 0, 'error starting program'                   # shouldn't return
    else:
        print 'Child is', pid
        if raw_input() == 'q': break
