#!/usr/local/bin/python

from Tkinter  import *                                 # widgets, constants
from guitools import frame, button, entry              # widget builders


class OperandButton(Button):
    def __init__(self, parent, text, char):
        self.text = text
        self.char = char
        Button.__init__(self, parent, text=char, command=self.press)
        self.pack(side=LEFT, expand=YES, fill=BOTH)
    def press(self):
        self.text.set( self.text.get() + self.char )     # show my char


class CalcGui(Frame):
    def __init__(self):                                # an extended frame
        Frame.__init__(self)                           # on default top-level
        self.pack(expand=YES, fill=BOTH)               # all parts expandable
        self.master.title('Python Calculator 0.1')     # 6 frames plus entry
        self.master.iconname("pcalc1")

        self.names = {}                                # namespace for variables
        text = StringVar()
        entry(self, TOP, text)

        rows = ["abcd", "0123", "4567", "89()"]
        for row in rows:
            frm = frame(self, TOP)
            for char in row: OperandButton(frm, text, char)

        frm = frame(self, TOP)
        for char in "+-*/=": OperandButton(frm, text, char)

        frm = frame(self, BOTTOM)
        button(frm, LEFT, 'eval',  lambda x=self, y=text: x.eval(y) )
        button(frm, LEFT, 'clear', lambda x=text: x.set('') )

    def eval(self, text):
        try:
            text.set(`eval(text.get(), self.names, self.names)`)
        except SyntaxError:
            try:
                exec(text.get(), self.names, self.names)  
            except:
                text.set("ERROR")         # bad as statement too?
            else:
                text.set('')              # worked as a statement
        except:
            text.set("ERROR")             # other eval expression errors

if __name__ == '__main__': CalcGui().mainloop()
