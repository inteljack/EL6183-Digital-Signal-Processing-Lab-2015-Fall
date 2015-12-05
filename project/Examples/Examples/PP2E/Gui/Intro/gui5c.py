from Tkinter import *

class HelloButton(Button):
    def __init__(self, parent=None, side=TOP, **config):  # add callback method
        Button.__init__(self, parent, config)             # and pack myself
        self.pack(side=side)                              # allow passed side
        self.config(command=self.callback)
    def callback(self):                             
        print 'Goodbye world...'                   
        self.quit()
 
if __name__ == '__main__':
    HelloButton(side=LEFT, text='Hello subclass world').mainloop()
