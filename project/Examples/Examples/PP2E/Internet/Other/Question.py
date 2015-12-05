# Python applet file: Question.py
# in the same location (URL) as the html file
# that references it; adds widgets to browser;

from Tkinter import *

class Question:                          # run by grail?
    def __init__(self, parent):          # parent=browser
        self.button = Button(parent, 
                             bitmap='question',
                             command=self.action)
        self.button.pack()

    def action(self):
        if self.button['bitmap'] == 'question':
            self.button.config(bitmap='questhead')
        else:
            self.button.config(bitmap='question')

if __name__ == '__main__':
    root = Tk()                    # run stand-alone?
    button = Question(root)        # parent=Tk: top-level
    root.mainloop()
