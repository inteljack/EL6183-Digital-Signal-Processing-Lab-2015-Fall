# wrap command-line script in GUI redirection tool to popup its output

from Tkinter import *
from packdlg import runPackDialog
from PP2E.Gui.Tools.guiStreams import redirectedGuiFunc

def runPackDialog_Wrapped():
    redirectedGuiFunc(runPackDialog)    # wrap entire callback handler

if __name__ == '__main__':
    root = Tk()
    Button(root, text='pop', command=runPackDialog_Wrapped).pack(fill=X)
    root.mainloop()
