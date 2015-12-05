from Tkinter import *

class HelloButton(Button):
    def __init__(self, parent=None, config={}):   # add callback method
        Button.__init__(self, parent, config)     # use a real dictionary
        self.pack()
        self.config(command=self.callback)
    def callback(self):                                 
        print 'Goodbye world...' 
        self.quit()
 
if __name__ == '__main__':
    HelloButton(None, {'text': 'Hello subclass world'}).mainloop()
