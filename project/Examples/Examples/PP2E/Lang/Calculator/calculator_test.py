##########################################################################
# test calculator use as an extended and embedded gui component;
##########################################################################

from Tkinter import *
from calculator import CalcGui
from PP2E.Dbase.TableBrowser.guitools import *

def calcContainer(parent=None):
    frm = Frame(parent)       
    frm.pack(expand=YES, fill=BOTH)
    Label(frm, text='Calc Container').pack(side=TOP)
    CalcGui(frm)
    Label(frm, text='Calc Container').pack(side=BOTTOM)
    return frm

class calcSubclass(CalcGui): 
    def makeWidgets(self, fg, bg, font):
        Label(self, text='Calc Subclass').pack(side=TOP)
        Label(self, text='Calc Subclass').pack(side=BOTTOM)
        CalcGui.makeWidgets(self, fg, bg, font)
        #Label(self, text='Calc Subclass').pack(side=BOTTOM)

if __name__ == '__main__': 
    import sys
    if len(sys.argv) == 1:            # % calculator_test.py
        root = Tk()                   # run 3 calcs in same process
        CalcGui(Toplevel())           # each in a new toplevel window
        calcContainer(Toplevel())
        calcSubclass(Toplevel()) 
        Button(root, text='quit', command=root.quit).pack()
        root.mainloop()
    if len(sys.argv) == 2:            # % calculator_testl.py -
        CalcGui().mainloop()          # as a standalone window (default root)
    elif len(sys.argv) == 3:          # % calculator_test.py - - 
        calcContainer().mainloop()    # as an embedded component
    elif len(sys.argv) == 4:          # % calculator_test.py - - - 
        calcSubclass().mainloop()     # as a customized superclass
