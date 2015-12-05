############################################################
# spawn a child process/program, connect my stdin/stdout
# to child process's stdout/stdin -- my reads and writes 
# map to output and input streams of the spawned program;
# much like popen2.popen2 plus parent stream redirection;
############################################################

import os, sys

def spawn(prog, *args):                       # pass progname, cmdline args 
    stdinFd  = sys.stdin.fileno()             # get descriptors for streams
    stdoutFd = sys.stdout.fileno()            # normally stdin=0, stdout=1

    parentStdin, childStdout  = os.pipe()     # make two ipc pipe channels
    childStdin,  parentStdout = os.pipe()     # pipe returns (inputfd, outoutfd)
    pid = os.fork()                           # make a copy of this process
    if pid:
        os.close(childStdout)                 # in parent process after fork:
        os.close(childStdin)                  # close child ends in parent
        os.dup2(parentStdin,  stdinFd)        # my sys.stdin copy  = pipe1[0]
        os.dup2(parentStdout, stdoutFd)       # my sys.stdout copy = pipe2[1]
    else:
        os.close(parentStdin)                 # in child process after fork:
        os.close(parentStdout)                # close parent ends in child
        os.dup2(childStdin,  stdinFd)         # my sys.stdin copy  = pipe2[0]
        os.dup2(childStdout, stdoutFd)        # my sys.stdout copy = pipe1[1]
        args = (prog,) + args
        os.execvp(prog, args)                 # new program in this process
        assert 0, 'execvp failed!'            # os.exec call never returns here

if __name__ == '__main__':
    mypid = os.getpid()
    spawn('python', 'pipes-testchild.py', 'spam')    # fork child program

    print 'Hello 1 from parent', mypid               # to child's stdin
    sys.stdout.flush()                               # subvert stdio buffering
    reply = raw_input()                              # from child's stdout
    sys.stderr.write('Parent got: "%s"\n' % reply)   # stderr not tied to pipe!    

    print 'Hello 2 from parent', mypid
    sys.stdout.flush()
    reply = sys.stdin.readline()
    sys.stderr.write('Parent got: "%s"\n' % reply[:-1])    

