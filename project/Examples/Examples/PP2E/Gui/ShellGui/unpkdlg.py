# added file select dialog, handles cancel better

from Tkinter import *                                     # widget classes
from tkFileDialog import *                                # file open dialog
from PP2E.System.App.Clients.unpackapp import UnpackApp   # use unpack class

def runUnpackDialog():
    input = UnpackDialog().input                  # get input from GUI
    if input != '':                               # do non-gui file stuff
        print 'UnpackApp:', input
        app = UnpackApp(ifile=input)              # run with input from file
        app.main()                                # execute app class 

class UnpackDialog(Toplevel):
    def __init__(self):                           # a function would work too
        Toplevel.__init__(self)                   # resizable root box
        self.input = ''                           # a label and an entry
        self.title('Enter Unpack Parameters')
        Label(self, text='input file?', relief=RIDGE, width=11).pack(side=LEFT)
        e = Entry(self, relief=SUNKEN) 
        b = Button(self, text='browse...')
        e.bind('<Key-Return>', self.gotit)
        b.config(command=(lambda x=e: x.insert(0, askopenfilename())))
        b.pack(side=RIGHT)
        e.pack(side=LEFT, expand=YES, fill=X)
        self.entry = e
        self.grab_set()                   # make myself modal
        self.focus_set()
        self.wait_window()                # till I'm destroyed on return->gotit
    def gotit(self, event):               # on return key: event.widget==Entry
        self.input = self.entry.get()     # fetch text, save in self
        self.destroy()                    # kill window, but instance lives on
    
if __name__ == "__main__":
    Button(None, text='pop', command=runUnpackDialog).pack()
    mainloop()
