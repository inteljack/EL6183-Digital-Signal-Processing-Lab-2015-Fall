############################################################
# start up 10 copies of child.py running in parallel;
# use spawnv to launch a program on Windows (like fork+exec)
# P_OVERLAY replaces, P_DETACH makes child stdout go nowhere
############################################################

import os, sys
 
for i in range(10):
    if sys.platform[:3] == 'win':
        pypath  = r'C:\program files\python\python.exe'
        os.spawnv(os.P_NOWAIT, pypath, ('python', 'child.py', str(i)))
    else:
        pid = os.fork()
        if pid != 0:
            print 'Process %d spawned' % pid
        else:
            os.execlp('python', 'python', 'child.py', str(i))
print 'Main process exiting.'