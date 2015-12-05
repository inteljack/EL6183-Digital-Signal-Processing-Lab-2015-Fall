############################################################
# 
# ***PLEASE NOTE: THIS IS NEITHER COMPLETE NOR CORRECT***
#
# adds support for shell cmd runs, nonblocking func calls, 
# stay-up output displays;  to do: make input come from a
# stay-up entry field, not a popup per line;
# warning: redirect func resets stdin/out for entire
# process--may lead to odd behaviour (if not blocking);
# also possible: Tk file event handler, but 
# doesn't yet work on MS-Windows under Tk 8.0;
# gui shell cmd could also reset sys.stdout and use print,
# but that resets stdout for entire process;
# if no gui AppActive: mainloop() (now assumes is);
# could 'return output' too, but just assume that caller
# will create a box and pass in, if it is to be processed
# after the redirect utility call;
############################################################

from Tkinter import *
from guiStreams import GuiInput, GuiOutput
import os, sys, thread

# 
# client tools
# 

BLOCK, THREAD, ONIDLE = 'block', 'thread', 'onidle'

def redirectGuiFunc(func, pargs, kargs, mode=BLOCK, currBox=None):
    streams    = sys.stdin, sys.stdout
    sys.stdin  = GuiInput()                            # run func with its
    sys.stdout = currBox or GuiOutput(Toplevel())      # stdin/out streams
    if mode == BLOCK:                                  # set to gui devices
        apply(func, pargs, kargs)
        sys.stdin, sys.stdout = streams
    elif mode == ONIDLE:
        def runner(func, pargs, kargs, streams=streams):
            apply(func, pargs, kargs)
            sys.stdin, sys,stdout = streams
        sys.stdout.after_idle(apply, runner, pargs, kargs)
    elif mode == THREAD: 
        def runner(func, pargs, kargs, streams=streams):
            apply(func, pargs, kargs)
            sys.stdin, sys,stdout = streams
        thread.start_new_thread(runner, (func, pargs, kargs))
    else:
        assert 0, 'Bad run mode' 

def redirectGuiShellCmd(command, mode=THREAD, currBox=None):
    input  = os.popen(command, 'r')
    output = currBox or GuiOutput(Toplevel())
    def reader(input, output):                      # show shell command
        while 1:                                    # output in a popup
            line = input.readline()                 # text box widget
            if not line: break
            output.write(line)
    if mode == BLOCK:
        reader(input, output)
    elif mode == ONIDLE:
        output.after_idle(reader, input, output)
    elif mode == THREAD:
        thread.start_new_thread(reader, (input, output))
    else:
        assert 0, 'Bad run mode'

class GuiOutputBox(Toplevel):
    def __init__(self, parent=None):
        Toplevel.__init__(self, parent)            # single window model
        self.box = GuiOutput(self)                 # embed an output frame 
    def runShellCmd(self, cmd, mode=THREAD):
        redirectGuiShellCmd(cmd, mode, self.box)
    def runFunction(self, func, pargs, kargs, mode=BLOCK):
        redirectGuiFunc(func, pargs, kargs, mode, self.box)
    def write(self, line):
        self.box.write(line)

# 
# self-test logic
#

def _selfTest():                                    # an enclosing gui app
    def interact(number=5):                         # runs a non-gui function
        print 'Starting interact'                   # and non-gui shell commands
        while 1:
            try:
                input = raw_input('Enter value: ')
                print input, '*', number, 'is:', eval(input) * number
            except EOFError: 
                break
            except:
                print 'Bad number--try again'
        for i in xrange(100000000):
            if i % 10000 == 0: print i   # stress the cpu
        print 'Done'

    for mode in (THREAD, ONIDLE, BLOCK):
        Button(text='Shell ' + mode,
               command=lambda m=mode:
                         redirectGuiShellCmd('ls *.py', m)).pack(fill=X)

    for mode in (THREAD, ONIDLE, BLOCK):
        Button(text='Func ' + mode, 
               command=lambda m=mode, i=interact:
                         redirectGuiFunc(i, (4,), {}, m)).pack(fill=X)

    def existingBox1():
        win = Toplevel()
        box = GuiOutput(win)
        box.pack()
        Button(win, text='OK', command=win.destroy).pack()  # erase window
        box.write('--Hello GuiStreams world--\n')
        redirectGuiShellCmd('ls *.py', BLOCK, box)
        box.write('--Second command--\n')
        redirectGuiShellCmd('ls *.txt', BLOCK, box)
        box.write('--Command finished--\n')

    def existingBox2(interact=interact):
        win = GuiOutputBox()
        Button(win, text='OK', command=win.destroy).pack()  # erase window
        win.write('--Hello GuiStreams world--\n')
        win.runShellCmd('ls *.py', BLOCK)
        win.write('--Second command--\n')
        win.runShellCmd('ls *.txt', BLOCK)
        win.write('--Function--\n')
        win.runFunction(interact, (), {})
        win.write('--Command finished--\n')

    Button(text='Shell box1', command=existingBox1).pack(fill=X)
    Button(text='Shell box2', command=existingBox2).pack(fill=X)
    mainloop()

if __name__ == '__main__': _selfTest()
