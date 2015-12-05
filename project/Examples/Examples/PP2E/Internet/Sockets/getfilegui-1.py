##########################################################
# launch getfile script client from simple Tkinter GUI;
# could also or os.fork+exec, os.spawnv (see Launcher);
# windows: replace 'python' with 'start' if not on path; 
##########################################################

import sys, os
from Tkinter import *
from tkMessageBox import showinfo

def onReturnKey():
    cmdline = ('python getfile.py -mode client -file %s -port %s -host %s' %
                      (content['File'].get(),
                       content['Port'].get(), 
                       content['Server'].get()))
    os.system(cmdline)
    showinfo('getfilegui-1', 'Download complete')

box = Frame(Tk())
box.pack(expand=YES, fill=X)
lcol, rcol = Frame(box), Frame(box)
lcol.pack(side=LEFT)
rcol.pack(side=RIGHT, expand=Y, fill=X)

labels = ['Server', 'Port', 'File']
content = {}
for label in labels:
    Label(lcol, text=label).pack(side=TOP)
    entry = Entry(rcol)
    entry.pack(side=TOP, expand=YES, fill=X)
    content[label] = entry

box.master.title('getfilegui-1')
box.master.bind('<Return>', (lambda event: onReturnKey()))
mainloop()
