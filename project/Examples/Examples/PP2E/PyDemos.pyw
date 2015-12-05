##############################################################################
# PyDemos.pyw
# Programming Python, 2nd Edition (PP2E), 1999--2001
#
# Launch major Python+Tk GUI examples from the book, in a 
# platform-neutral way.  This file also serves as an index
# to major program examples, though many book examples aren't
# GUI-based, and so aren't listed here (e.g., see the Linux 
# gcc build scripts in the examples root directory for C 
# integration program pointers).  Also see: 
#
# - PyGadgets.py, a simpler script for starting programs in 
#   non-demo mode that you wish to use on a regular basis 
# - PyGadgets_bar.pyw, which creates a button bar for starting 
#   all PyGadgets programs on demand, not all at once 
# - Launcher.py for starting programs without environment 
#   settings--finds Python, sets PYTHONPATH, etc.
# - Launch_*.py for starting PyDemos and PyGadgets with 
#   Launcher.py--run these for a quick look
# - LaunchBrowser.py for running example web pages with an
#   automatically-located web browser
# - README-PP2E.txt, for general examples information
#
# Internet-based demos live here:
#     http://starship.python.net/~lutz/PyInternetDemos.html
# but this program tries to start a browser on the main web pages
# automatically, either on the site above or on local page files.
# Additional program comments were moved to file PyDemos.doc.txt
##############################################################################

import sys, time, os, launchmodes
from Tkinter import *

# -live loads root pages off net, -file loads local files
InternetMode = '-file' 

##################################
# start building main gui windows
##################################

Root = Tk()
Root.title('PP2E Demos')

# build message window
Stat = Toplevel()
Stat.protocol('WM_DELETE_WINDOW', lambda:0)    # ignore wm delete
Stat.title('PP2E demo info')

Info = Label(Stat, text = 'Select demo',
             font=('courier', 20, 'italic'), padx=12, pady=12, bg='lightblue')
Info.pack(expand=YES, fill=BOTH)

#############################################
# add launcher buttons with callback objects
#############################################

# demo launcher class
class Launcher(launchmodes.PortableLauncher):    # use wrapped launcher class
    def announce(self, text):                    # customize to set GUI label
        Info.config(text=text)

def demoButton(name, what, where):
    b = Button(Root, bg='navy', fg='white', relief=RIDGE, border=4)
    b.config(text=name, command=Launcher(what, where))
    b.pack(side=TOP, expand=YES, fill=BOTH)

demoButton('PyEdit',        
           'Text file editor',                              # edit myself
           'Gui/TextEditor/textEditor.pyw PyDemos.pyw')     # assume in cwd
demoButton('PyView',        
           'Image slideshow, plus note editor',
           'Gui/SlideShow/slideShowPlus.py Gui/gifs')
demoButton('PyDraw',                    
           'Draw and move graphics objects', 
           'Gui/MovingPics/movingpics.py Gui/gifs') 
demoButton('PyTree',                              
           'Tree data structure viewer',
           'Dstruct/TreeView/treeview.py')
demoButton('PyClock',                             
           'Analog/digital clocks',
           'Gui/Clock/clockStyles.py Gui/gifs')   
demoButton('PyToe',     
           'Tic-tac-toe game (AI)',
           'Ai/TicTacToe/tictactoe.py') 
demoButton('PyForm',                                    # view in-memory dict
           'Persistent table viewer/editor',            # or cwd shelve of class
           'Dbase/TableBrowser/formgui.py')             # 0=do not reinit shelve
          #'Dbase/TableBrowser/formtable.py  shelve 0 pyformData-1.5.2') 
          #'Dbase/TableBrowser/formtable.py  shelve 1 pyformData') 
demoButton('PyCalc',    
           'Calculator, plus extensions',
           'Lang/Calculator/calculator_plusplus.py')
demoButton('PyMail',  
           'Python+Tk pop/smtp email client',
           'Internet/Email/PyMailGui.py')
demoButton('PyFtp',  
           'Python+Tk ftp clients',
           'Internet/Ftp/PyFtpGui.pyw')

if InternetMode == '-file':
    pagepath = os.getcwd() + '/Internet/Cgi-Web'
    demoButton('PyErrata',  
               'Internet-based errata report system',
               'LaunchBrowser.py -file %s/PyErrata/pyerrata.html' % pagepath)
    demoButton('PyMailCgi',  
               'Browser-based pop/smtp email interface',
               'LaunchBrowser.py -file %s/PyMailCgi/pymailcgi.html' % pagepath)
    demoButton('PyInternet',
               'Internet-based demo launcher page',
               'LaunchBrowser.py -file %s/PyInternetDemos.html' % pagepath)
else:
    site = 'starship.python.net/~lutz'
    demoButton('PyErrata',  
               'Internet-based errata report system',
               'LaunchBrowser.py -live PyErrata/pyerrata.html ' + site)
    demoButton('PyMailCgi',  
               'Browser-based pop/smtp email interface',
               'LaunchBrowser.py -live PyMailCgi/pymailcgi.html ' + site)
    demoButton('PyInternet',
               'Main Internet demos launcher page',
               'LaunchBrowser.py -live PyInternetDemos.html ' + site)

#To try: bind mouse entry events to change info text when over a button
#See also: site http://starship.python.net/~lutz/PyInternetDemos.html

#############################################
# toggle info message box font once a second
#############################################

def refreshMe(info, ncall):
    slant = ['normal', 'italic', 'bold', 'bold italic'][ncall % 4]
    info.config(font=('courier', 20, slant))
    Root.after(1000, (lambda info=info, ncall=ncall: refreshMe(info, ncall+1)) )

########################################
# unhide/hide status box on info clicks
########################################

Stat.iconify()
def onInfo():
    if Stat.state() == 'iconic':
        Stat.deiconify()
    else:
        Stat.iconify()  # was 'normal'

############################################
# popup a few web link buttons if connected
############################################

radiovar = StringVar() # use a global

def onLinks():
    popup = Toplevel()
    popup.title('PP2E web site links')
    links = [("Book",     'LaunchBrowser.py -live about-pp.html rmi.net/~lutz'),
             ("Python",   'LaunchBrowser.py -live index.html www.python.org'),
             ("O'Reilly", 'LaunchBrowser.py -live index.html www.oreilly.com'),
             ("Author",   'LaunchBrowser.py -live index.html rmi.net/~lutz')]

    for (name, command) in links:
        callback = Launcher((name + "'s web site"), command)
        link = Radiobutton(popup, text=name, command=callback)
        link.config(relief=GROOVE, variable=radiovar, value=name)
        link.pack(side=LEFT, expand=YES, fill=BOTH)
    Button(popup, text='Quit', command=popup.destroy).pack(expand=YES,fill=BOTH)

    if InternetMode != '-live':
        from tkMessageBox import showwarning
        showwarning('PP2E Demos', 'Web links require an Internet connection')

#############################################
# finish building main gui, start event loop
#############################################

Button(Root, text='Info',  command=onInfo).pack(side=TOP, fill=X)
Button(Root, text='Links', command=onLinks).pack(side=TOP, fill=X)
Button(Root, text='Quit',  command=Root.quit).pack(side=BOTTOM, fill=X)
refreshMe(Info, 0)  # start toggling
Root.mainloop()
