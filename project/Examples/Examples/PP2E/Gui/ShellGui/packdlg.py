# added file select dialogs, empties test; could use grids

import string
from glob import glob                                   # filename expansion
from Tkinter import *                                   # gui widget stuff
from tkFileDialog import *                              # file selector dialog
from PP2E.System.App.Clients.packapp import PackApp     # use pack class

def runPackDialog():
    s1, s2 = StringVar(), StringVar()          # run class like a function
    PackDialog(s1, s2)                         # pop-up dialog: sets s1/s2
    output, patterns = s1.get(), s2.get()      # whether 'ok' or wm-destroy
    if output != "" and patterns != "":
        patterns = string.split(patterns)
        filenames = []
        for sublist in map(glob, patterns):    # do expansion manually
            filenames = filenames + sublist    # Unix does auto on command-line
        print 'PackApp:', output, filenames
        app = PackApp(ofile=output)            # run with redirected output
        app.args = filenames                   # reset cmdline args list
        app.main()                             # should show msgs in gui too

class PackDialog(Toplevel):
    def __init__(self, target1, target2):
        Toplevel.__init__(self)                  # a new top-level window
        self.title('Enter Pack Parameters')      # 2 frames plus a button

        f1 = Frame(self) 
        l1 = Label(f1,  text='Output file?', relief=RIDGE, width=15)
        e1 = Entry(f1,  relief=SUNKEN) 
        b1 = Button(f1, text='browse...') 
        f1.pack(fill=X)
        l1.pack(side=LEFT)
        e1.pack(side=LEFT, expand=YES, fill=X)
        b1.pack(side=RIGHT)
        b1.config(command= (lambda x=target1: x.set(askopenfilename())) )

        f2 = Frame(self)
        l2 = Label(f2,  text='Files to pack?', relief=RIDGE, width=15)
        e2 = Entry(f2,  relief=SUNKEN) 
        b2 = Button(f2, text='browse...') 
        f2.pack(fill=X)
        l2.pack(side=LEFT)
        e2.pack(side=LEFT, expand=YES, fill=X)
        b2.pack(side=RIGHT)
        b2.config(command=
                 (lambda x=target2: x.set(x.get() +' '+ askopenfilename())) )

        Button(self, text='OK', command=self.destroy).pack()
        e1.config(textvariable=target1)
        e2.config(textvariable=target2)

        self.grab_set()         # make myself modal:
        self.focus_set()        # mouse grab, keyboard focus, wait...
        self.wait_window()      # till destroy; else returns to caller now

if __name__ == '__main__':
    root = Tk()
    Button(root, text='pop', command=runPackDialog).pack(fill=X)
    Button(root, text='bye', command=root.quit).pack(fill=X) 
    root.mainloop()
