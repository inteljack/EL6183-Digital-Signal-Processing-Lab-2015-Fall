from Tkinter import *	

class Hello(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        Button(self, {'text': 'message1',
                      'command': self.message1, Pack: {'side':'left'} })
        Button(self, {'text': 'message2',
                      'command': self.message2, Pack: {'side':'right'} })

    def message1(self):
        import rad1
        reload(rad1)       # reloading this module itself has no effect!
        print 'MESSAGE1'   # already made a Hello and registered bound-methods

    def message2(self):
        import rad1
        reload(rad1)
        print 'MESSAGE2'    
    
if __name__ == '__main__': Hello().mainloop()    # 'if' or adds new buttons too
