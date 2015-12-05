#!/bin/env python
####################################################################
# Start various examples; run me at system boot time to make them
# always available.  This file is meant for starting programs you
# actually wish to use; see PyDemos for starting Python/Tk demos 
# and more details on program start options.  Windows usage note: 
# this is a '.py' file, so you get a dos box console window when it
# is clicked; the dos box is used to show a startup message (and we
# sleep 5 seconds to make sure it's visible while gadgets start up).
# If you don't want the dos popup, run with the 'pythonw' program 
# (not 'python'), use a '.pyw' suffix, mark with a 'run minimized' 
# Windows property, or spawn the file from elsewhere; see PyDemos.
####################################################################

import sys, time, os, time
from Tkinter import *
from launchmodes import PortableLauncher           # reuse program start class

def runImmediate(mytools):
    # launch gadget programs immediately
    print 'Starting Python/Tk gadgets...'          # msgs to temp stdout screen
    for (name, commandLine) in mytools:
        PortableLauncher(name, commandLine)()      # call now to start now
    print 'One moment please...'                   # \b means a backspace
    if sys.platform[:3] == 'win':
        # on Windows keep stdio console window up for 5 seconds
        for i in range(5): time.sleep(1); print ('\b' + '.'*10), 

def runLauncher(mytools):
    # put up a simple launcher bar for later use
    root = Tk()
    root.title('PyGadgets PP2E')
    for (name, commandLine) in mytools:
        b = Button(root, text=name, fg='black', bg='beige', border=2,
                   command=PortableLauncher(name, commandLine)) 
        b.pack(side=LEFT, expand=YES, fill=BOTH)
    root.mainloop()

mytools = [
    ('PyEdit',   'Gui/TextEditor/textEditor.pyw'),
    ('PyView',   'Gui/SlideShow/slideShowPlus.py Gui/gifs'),
    ('PyCalc',   'Lang/Calculator/calculator.py'),
    ('PyMail',   'Internet/Email/PyMailGui.py'),
    ('PyClock',  'Gui/Clock/clock.py -size 175 -bg white'
                          ' -picture Gui/gifs/pythonPowered.gif'),   
    ('PyToe',    'Ai/TicTacToe/tictactoe.py' 
                          ' -mode Minimax -fg white -bg navy'),
    ('PyNet',    'LaunchBrowser.py -file ' + os.getcwd() + 
                          '/Internet/Cgi-Web/PyInternetDemos.html')
]

if __name__ == '__main__':
    prestart, toolbar = 1, 0
    if prestart:
        runImmediate(mytools)
    if toolbar:
        runLauncher(mytools)
