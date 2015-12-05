# add file select dialog/button

from glob import glob                                 # filename expansion
from Tkinter import *                                 # gui widget stuff
from tkFileDialog import *                            # std file selector dialog
from PP2E.System.App.Clients.textpack import pack     # use pack function
from PP2E.System.Streams.redirect     import redirect # use stream redirector

class PackDialog(Toplevel):
    def __init__(self, target1, target2):
        Toplevel.__init__(self)                       # a new top-level window
        self.title('Enter Pack Parameters')           # 2 frames plus a button

        f1 = Frame(self) 
        f1.pack(expand=YES, fill=X)
        Label(f1, text='output file?', relief=RIDGE, width=15).pack(side=LEFT)
        e1 = Entry(f1, relief=SUNKEN) 
        e1.pack(side=RIGHT, expand=YES, fill=X)
        Button(text="browse...", 
               command=(lambda x=e1: x.set(askopenfilename()))).pack(side=RIGHT)

        f2 = Frame(self)
        f2.pack(expand=YES, fill=X)
        Label(f2, text='files to pack?', relief=RIDGE, width=15).pack(side=LEFT)
        e2 = Entry(f2, relief=SUNKEN) 
        e2.pack(side=RIGHT, expand=YES, fill=X)
        Button(text="browse...", 
               command=(lambda x=e2: x.set(askopenfilename()))).pack(side=RIGHT)

        Button(self, text='OK', command=self.destroy).pack()
        e1['textvariable'] = target1
        e2['textvariable'] = target2

        self.grab_set()         # make myself modal:
        self.focus_set()        # mouse grab, keyboard focus, wait...
        self.wait_window()      # till destroy; else returns to caller now

def packDialog():
    s1, s2 = StringVar(), StringVar()          # run class like a function
    PackDialog(s1, s2)                         # pop-up dialog: sets s1/s2
    output, pattern = s1.get(), s2.get()       # whether 'ok' or wm-destroy
    print 'pack:', output, pattern
    sys.args = ['pack.py'] + glob(pattern)     # fake command line for script
    packedtext = redirect(pack, (), '')        # should put messages in gui too
    open(output, 'w').write(packedtext)         

if __name__ == '__main__':
    class Outer(Frame):
        def __init__(self):
            Frame.__init__(self)
            self.pack()
            Button(self, text='pop', command=self.pop).pack()
            Button(self, text='hey', command=self.hey).pack()
        def pop(self): 
            packDialog()
        def hey(self): print 'HEY'      # make sure dialog is modal
    Outer().mainloop()
