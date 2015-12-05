from Tkinter import *

class frame(Frame):
    def __init__(self, root, side): 
        Frame.__init__(self, root)
        self.pack(side=side, expand=YES, fill=BOTH)

class label(Label):
    def __init__(self, root, side, text):
        Label.__init__(self, root, text=text, relief=RIDGE) 
        self.pack(side=side, expand=YES, fill=BOTH)

class button(Button):
    def __init__(self, root, side, text, command): 
        Button.__init__(self, root, text=text, command=command)
        self.pack(side=side, expand=YES, fill=BOTH)

class entry(Entry):
    def __init__(self, root, side, linkvar):
        Entry.__init__(self, root, relief=SUNKEN, textvariable=linkvar)
        self.pack(side=side, expand=YES, fill=BOTH)
