from Tkinter import *
from guitools import frame, button, entry

class CalcGui(Frame):
    def __init__(self):                                # an extended frame
        Frame.__init__(self)                           # on default top-level
        self.pack(expand=YES, fill=BOTH)               # all parts expandable
        self.master.title('Python Calculator 0.1')     # 6 frames plus entry
        self.master.iconname("pcalc1")

        self.names = {}        # namespace for variables
        text = StringVar()
        entry(self, TOP, text)

        frm = frame(self, RIGHT)
        for char in "+-*/=": button(frm, TOP, char,
                               lambda x=text, y=char: x.set(x.get()+' '+y+' '))

        rows = ["abcd", "0123", "4567", "89()"]
        for row in rows:
            frm = frame(self, TOP)
            for char in row: button(frm, LEFT, char, 
                               lambda x=text, y=char: x.set(x.get() + y))

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

