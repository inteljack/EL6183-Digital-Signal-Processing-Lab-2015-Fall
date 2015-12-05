###############################################################
# launch Python programs with reusable launcher scheme classes;
# assumes 'python' is on your system path (but see Launcher.py)
###############################################################

import sys, os, string
pycmd = 'python'   # assume it is on your system path

class LaunchMode:
    def __init__(self, label, command):
        self.what  = label
        self.where = command
    def __call__(self):                   # on call, ex: button press callback
        self.announce(self.what)
        self.run(self.where)              # subclasses must define run()
    def announce(self, text):             # subclasses may redefine announce()
        print text                        # methods instead of if/elif logic
    def run(self, cmdline):
        assert 0, 'run must be defined'

class System(LaunchMode):                          # run shell commands
    def run(self, cmdline):                        # caveat: blocks caller
        os.system('%s %s' % (pycmd, cmdline))      # unless '&' added on Linux

class Popen(LaunchMode):                           # caveat: blocks caller 
    def run(self, cmdline):                        # since pipe closed too soon
        os.popen(pycmd + ' ' + cmdline)            # 1.5.2 fails in Windows GUI

class Fork(LaunchMode):
    def run(self, cmdline):
        assert hasattr(os, 'fork')                 # for linux/unix today
        cmdline = string.split(cmdline)            # convert string to list
        if os.fork() == 0:                         # start new child process
            os.execvp(pycmd, [pycmd] + cmdline)    # run new program in child

class Start(LaunchMode):
    def run(self, cmdline):                        # for windows only
        assert sys.platform[:3] == 'win'           # runs independent of caller
        os.system('start ' + cmdline)              # uses Windows associations

class Spawn(LaunchMode):                           # for windows only
    def run(self, cmdline):                        # run python in new process
        assert sys.platform[:3] == 'win'           # runs independent of caller
       #pypath = r'C:\program files\python\python.exe'
        try:                                                # get path to python
            pypath = os.environ['PP2E_PYTHON_FILE']         # run by launcher?
        except KeyError:                                    # if so configs env
            from Launcher import which, guessLocation
            pypath = which('python.exe', 0) or guessLocation('python.exe', 1,0) 
        os.spawnv(os.P_DETACH, pypath, ('python', cmdline)) # P_NOWAIT: dos box 

class Top_level(LaunchMode):
    def run(self, cmdline):                           # new window, same process
        assert 0, 'Sorry - mode not yet implemented'  # tbd: need GUI class info

if sys.platform[:3] == 'win':
    PortableLauncher = Spawn            # pick best launcher for platform
else:                                   # need to tweak this code elsewhere
    PortableLauncher = Fork

class QuietPortableLauncher(PortableLauncher):
    def announce(self, text):
        pass

def selftest():
    myfile  = 'launchmodes.py'
    program = 'Gui/TextEditor/textEditor.pyw ' + myfile       # assume in cwd
    raw_input('default mode...')
    launcher = PortableLauncher('PyEdit', program)
    launcher()                                                # no block

    raw_input('system mode...')
    System('PyEdit', program)()                               # blocks

    raw_input('popen mode...')
    Popen('PyEdit', program)()                                # blocks

    if sys.platform[:3] == 'win':
        raw_input('DOS start mode...')                        # no block
        Start('PyEdit', program)()

if __name__ == '__main__': selftest()

