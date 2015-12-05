#!/usr/bin/python
import rexec, sys
Test = 1
if sys.platform[:3] == 'win':
    SafeDir = r'C:\temp'
else:
    SafeDir = '/tmp/'

def commandLine(prompt='Input (ctrl+z=end) => '):
    input = ''
    while 1:
        try:
            input = input + raw_input(prompt) + '\n'
        except EOFError:
            break
    print # clear for Windows
    return input

if not Test:
    import cgi                         # run on the web? - code from form
    form  = cgi.FieldStorage()         # else input interactively to test
    input = form['input'].value
else:
    input = commandLine()

# subclass to customize default rules: default=write modes disallowed
class Guard(rexec.RExec):
    def r_open(self, name, mode='r', bufsz=-1):
        if name[:len(SafeDir)] != SafeDir:
            raise SystemError, 'files outside %s prohibited' % SafeDir
        else:
            return open(name, mode, bufsz)

# limit system resources (not available on Windows)
if sys.platform[:3] != 'win':
    import resource            # at most 5 cpu seconds
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))

# run code string safely
guard = Guard()
guard.r_exec(input)      # ask guard to check and do opens
