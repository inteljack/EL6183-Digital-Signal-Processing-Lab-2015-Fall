################################################################################
# App subclasses for redirecting standard streams to files
################################################################################

import sys
from PP2E.System.App.Bases.app import App

################################################################################
# an app with input/output stream redirection
################################################################################

class StreamApp(App):
    def __init__(self, ifile='-', ofile='-'):
        App.__init__(self)                              # call superclass init
        self.setInput( ifile or self.name + '.in')      # default i/o file names
        self.setOutput(ofile or self.name + '.out')     # unless '-i', '-o' args

    def closeApp(self):                                 # not __del__
        try:
            if self.input != sys.stdin:                 # may be redirected
                self.input.close()                      # iff still open
        except: pass
        try:
            if self.output != sys.stdout:               # don't close stdout!
                self.output.close()                     # input/output exist?
        except: pass

    def help(self):
        App.help(self)
        print '-i <input-file |"-">  (default: stdin  or per app)'
        print '-o <output-file|"-">  (default: stdout or per app)'

    def setInput(self, default=None):
        file = self.getarg('-i') or default or '-'
        if file == '-':
            self.input = sys.stdin
            self.input_name = '<stdin>'
        else:
            self.input = open(file, 'r')            # cmdarg | funcarg | stdin
            self.input_name = file                  # cmdarg '-i -' works too

    def setOutput(self, default=None):
        file = self.getarg('-o') or default or '-'
        if file == '-':
            self.output = sys.stdout
            self.output_name = '<stdout>'
        else:
            self.output = open(file, 'w')           # error caught in main()
            self.output_name = file                 # make backups too?

class RedirectApp(StreamApp):
    def __init__(self, ifile=None, ofile=None):
        StreamApp.__init__(self, ifile, ofile)
        self.streams = sys.stdin, sys.stdout
        sys.stdin    = self.input                 # for raw_input, stdin
        sys.stdout   = self.output                # for print, stdout

    def closeApp(self):                           # not __del__
        StreamApp.closeApp(self)                  # close files?
        sys.stdin, sys.stdout = self.streams      # reset sys files


############################################################
# to add as a mix-in (or use multiple-inheritance...)
############################################################

class RedirectAnyApp:
    def __init__(self, superclass, *args):
        apply(superclass.__init__, (self,) + args)
        self.super   = superclass
        self.streams = sys.stdin, sys.stdout
        sys.stdin    = self.input                 # for raw_input, stdin
        sys.stdout   = self.output                # for print, stdout

    def closeApp(self):                         
        self.super.closeApp(self)                 # do the right thing
        sys.stdin, sys.stdout = self.streams      # reset sys files

