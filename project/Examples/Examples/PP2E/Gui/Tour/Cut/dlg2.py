from Tkinter import *
from tkMessageBox import askyesno, showerror

class NewDialogDemo(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        Pack.config(self)
        self.createWidgets()

    def greet(self):
        print "hi"

    def createWidgets(self):
        Label(self,  text='Hello popup world').pack(side=TOP)
        Button(self, text='Pop1', command=self.dialog1).pack()
        Button(self, text='Pop2', command=self.dialog2).pack()
        Button(self, text='Hey',  command=self.greet  ).pack(side=LEFT)
        Button(self, text='Bye',  command=self.quit   ).pack(side=RIGHT)

    def dialog1(self):
        ans = askyesno('Popup Fun!', 
                       'An example of a popup-dialog box.\n'
                       '"tkMessageBox" has a simple \n'
                       'interface for canned dialogs.')
        if ans: self.dialog2()

    def dialog2(self):
        showerror('HAL-9000', "I'm afraid I can't let you do that, Dave...")

if __name__ == '__main__': NewDialogDemo().mainloop()
