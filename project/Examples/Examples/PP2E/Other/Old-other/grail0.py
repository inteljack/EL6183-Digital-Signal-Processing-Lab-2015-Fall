# file: Question.py
# in the same location (URL) as the html file 
# that references it; adds widgets to browser;

from Tkinter import *

class Question:                                       # run by grail?
    def __init__(self, master):                       # master=browser
        self.button = Button(master,                  # add a new button
                             bitmap='question',
                             command=self.action)     # callback handler
        self.button.pack()

    def action(self):
        if self.button['bitmap'] == 'question':       # toggle image
            self.button.config(bitmap='questhead')    # on each press
        else:
            self.button.config(bitmap='question')

if __name__ == '__main__': 
    root = Tk()                           # run stand-alone?
    button = Question(root)               # master=Tk: default top-level
    root.mainloop()
