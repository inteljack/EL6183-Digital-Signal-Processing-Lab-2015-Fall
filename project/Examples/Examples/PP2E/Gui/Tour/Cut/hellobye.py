from Tkinter      import *              # get basic Tk widgets
from tkMessageBox import askokcancel    # get canned dialog
from hello        import Hello          # get the 'Hello' class

class HelloGoodbye(Hello):
    def make_widgets(self):             # extend superclass method
        Hello.make_widgets(self) 
        extra = Button(self, text='Goodbye', command=self.really_quit)
        extra.pack(side=RIGHT)
    
    def really_quit(self):
        Hello.quit(self)                # do superclass quit
    
    def quit(self):                     # redefine quit here
        ans = askokcancel('Verify exit', "I can't let you do that, Dave.")
        if ans: 
            self.really_quit()

if __name__ == '__main__':  HelloGoodbye().mainloop()

