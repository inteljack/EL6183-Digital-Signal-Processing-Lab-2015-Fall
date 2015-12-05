##############################################################################
# first-cut implementation of file-like classes that can be used to redirect
# input and output streams to GUI displays; as is, input comes from a common
# dialog popup (a single output+input interface or a persistent Entry field
# for input would be better); this also does not properly span lines for read 
# requests with a byte count > len(line); see guiStreamsTools.py for more;
##############################################################################

from Tkinter import *
from ScrolledText import ScrolledText
from tkSimpleDialog import askstring

class GuiOutput:
    def __init__(self, parent=None):
        self.text = None
        if parent: self.popupnow(parent)         # popup now or on first write
    def popupnow(self, parent=None):             # in parent now, Toplevel later
        if self.text: return
        self.text = ScrolledText(parent or Toplevel())
        self.text.config(font=('courier', 9, 'normal'))
        self.text.pack()
    def write(self, text):
        self.popupnow()
        self.text.insert(END, str(text))
        self.text.see(END)
        self.text.update()
    def writelines(self, lines):                 # lines already have '\n'
        for line in lines: self.write(line)      # or map(self.write, lines)

class GuiInput:
    def __init__(self):
        self.buff = ''
    def inputLine(self):
        line = askstring('GuiInput', 'Enter input line + <crlf> (cancel=eof)')
        if line == None:
            return ''                            # popup dialog for each line
        else:                                    # cancel button means eof
            return line + '\n'                   # else add end-line marker
    def read(self, bytes=None):
        if not self.buff:
            self.buff = self.inputLine()
        if bytes:                                # read by byte count
            text = self.buff[:bytes]             # doesn't span lines
            self.buff = self.buff[bytes:]
        else:
            text = ''                            # read all till eof
            line = self.buff
            while line:
                text = text + line
                line = self.inputLine()          # until cancel=eof=''
        return text 
    def readline(self):
        text = self.buff or self.inputLine()     # emulate file read methods
        self.buff = ''
        return text
    def readlines(self): 
        lines = []                               # read all lines
        while 1:
            next = self.readline()
            if not next: break
            lines.append(next)
        return lines

def redirectedGuiFunc(func, *pargs, **kargs):
    import sys
    saveStreams = sys.stdin, sys.stdout          # map func streams to popups
    sys.stdin   = GuiInput()                     # pops up dialog as needed
    sys.stdout  = GuiOutput()                    # new output window per call
    sys.stderr  = sys.stdout
    result = apply(func, pargs, kargs)           # this is a blocking func call
    sys.stdin, sys.stdout = saveStreams
    return result

def redirectedGuiShellCmd(command):
    import os
    input  = os.popen(command, 'r')
    output = GuiOutput()
    def reader(input, output):                   # show a shell command's
        while 1:                                 # standard output in a new
            line = input.readline()              # popup text box widget
            if not line: break
            output.write(line)
    reader(input, output)

if __name__ == '__main__':
    import string
    def makeUpper():                             # use standard streams
        while 1:
            try:
                line = raw_input('Line? ')
            except: 
                break
            print string.upper(line)
        print 'end of file'

    def makeLower(input, output):                # use explicit files
        while 1:
            line = input.readline()
            if not line: break
            output.write(string.lower(line)) 
        print 'end of file'

    root = Tk()
    Button(root, text='test streams', 
           command=lambda: redirectedGuiFunc(makeUpper)).pack(fill=X)
    Button(root, text='test files  ',
           command=lambda: makeLower(GuiInput(), GuiOutput()) ).pack(fill=X)
    Button(root, text='test popen  ',
           command=lambda: redirectedGuiShellCmd('dir *')).pack(fill=X)
    root.mainloop()     
