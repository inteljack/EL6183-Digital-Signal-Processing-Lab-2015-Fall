################################################################################
# App subclasses that map input/output to internal strings
################################################################################

import sys, string
from PP2E.System.App.Bases.app import App
from PP2E.System.App.Kinds.fakefile import Input, Output

################################################################################
# an App that redirects input/output streams to internal files (strings)
################################################################################

class InternalApp(App):
    def __init__(self, text=''):
        App.__init__(self)                  # i/o reset to classes
        self.input  = Input(text)           # use internal string i/o
        self.output = Output() 
        self.input_name  = '<internal>'
        self.output_name = '<internal>'

    def stop(self): 
        App.stop(self)
        return self.output.text             # result = saved output

class RedirectInternalApp(InternalApp):
    def __init__(self, input=''):
        InternalApp.__init__(self, input)          # streams reset to strings
        self.streams = sys.stdin, sys.stdout
        sys.stdin    = self.input                  # for raw_input, stdin
        sys.stdout   = self.output                 # for print, stdout

    def closeApp(self):                            # not __del__
        sys.stdin, sys.stdout = self.streams       # may be redirected

