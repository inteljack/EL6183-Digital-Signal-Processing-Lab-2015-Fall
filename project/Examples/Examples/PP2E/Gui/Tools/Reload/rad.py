from Tkinter import *	
import actions              # get initial callback handlers

class Hello(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        Button(self, text='message1', command=self.message1).pack(side=LEFT)
        Button(self, text='message2', command=self.message2).pack(side=RIGHT)

    def message1(self):
        reload(actions)         # need to reload actions module before calling
        actions.message1()      # now new version triggered by pressing button

    def message2(self):
        reload(actions)         # changes to actions.py picked up by reload
        actions.message2(self)  # call the most recent version; pass self

    def method1(self):
        print 'exposed method...'       # called from actions function
    
Hello().mainloop()
