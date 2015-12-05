from Tkinter import *                                # get the Tk module

class Hello(Frame):                                  # subclass our app
    def __init__(self, parent=None, side=TOP):
        Frame.__init__(self, parent)                 # do superclass init
        self.pack(side=side)
        self.make_widgets()                          # attach our widgets

    def make_widgets(self):
        Button(self, 
            text='Hello framework world!', command=self.quit).pack(side=LEFT)

if __name__ == '__main__': Hello().mainloop()
