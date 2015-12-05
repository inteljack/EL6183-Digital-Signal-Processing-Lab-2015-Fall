############################################################
# do something simlar by forking process instead of threads
# this doesn't currently work on Windows, because it has no
# os.fork call; use os.spawnv to start programs on Windows 
# instead; spawnv is roughly like a fork+exec combination;
############################################################

import os, sys

if len(sys.argv) > 1:
    # child processes
    if sys.platform[:3] == 'win':
        for i in range(100): 
            output = open('test6.winout', 'a')
            output.write('[%s] => %s\n' % (os.getpid(), i))
            output.close()
        output = open('test6.winout', 'a')
        output.write('Child process %d exiting.\n' % os.getpid())
    else:
        # use shared sys.stdout
        for i in range(100): print '[%s] => %s' % (os.getpid(), i)
        print 'Child process %d exiting.' % os.getpid()

else:
    # parent process
    if sys.platform[:3] == 'win':
        output = open('test6.winout', 'w')
    for i in range(10):
        if sys.platform[:3] == 'win':
            path = r'C:\program files\python\python.exe'
            os.spawnv(os.P_DETACH, path, ('python', 'thread-basics6.py -child'))
        else:
            pid = os.fork()
            if pid != 0:
                print 'Process %d spawned' % pid
            else:
                os.execlp('python', 'python', 'thread-basics6.py', '-child')
    print 'Main process exiting.'

