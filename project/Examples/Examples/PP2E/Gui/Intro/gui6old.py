from Tkinter import *                                # get the Tk module

class Hello(Frame):                                  # subclass our app
    def __init__(self, parent=None, config={}):
        Frame.__init__(self, parent, config)         # do superclass init
        self.pack()
        self.make_widgets()                          # add our widgets

    def make_widgets(self):
        Button(self, {'text': 'Hello framework world!',
                      'command' : self.quit,  Pack: {'side': 'left'} })

if __name__ == '__main__': Hello().mainloop()
