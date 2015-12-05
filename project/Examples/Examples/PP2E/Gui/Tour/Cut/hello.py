from Tkinter import *                   # get widget classes

class Hello(Frame):                     # subclass our GUI
    def __init__(self, parent=None):    # constructor method
        Frame.__init__(self, parent)
        self.pack()
        self.make_widgets()

    def make_widgets(self):             # attach a button to 'me'
        widget = Button(self, text='Hello world', command=self.quit)
        widget.pack(side=LEFT)

if __name__ == '__main__':  Hello().mainloop()
