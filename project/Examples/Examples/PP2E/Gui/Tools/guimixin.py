########################################################
# a "mixin" class for other frames: common methods for
# canned-dialogs, spawning programs, etc; must be mixed
# with a class derived from Frame for its quit method
########################################################

from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
from ScrolledText import ScrolledText
from PP2E.launchmodes import PortableLauncher, System

class GuiMixin:
    def infobox(self, title, text, *args):              # use standard dialogs
        return showinfo(title, text)                    # *args for bkwd compat
    def errorbox(self, text):
        showerror('Error!', text)
    def question(self, title, text, *args):
        return askyesno(title, text)

    def notdone(self):
        showerror('Not implemented', 'Option not available')
    def quit(self):
        ans = self.question('Verify quit', 'Are you sure you want to quit?')
        if ans == 1: 
            Frame.quit(self)                            # quit not recursive!
    def help(self):
        self.infobox('RTFM', 'See figure 1...')         # override this better

    def selectOpenFile(self, file="", dir="."):         # use standard dialogs
        return askopenfilename(initialdir=dir, initialfile=file)         
    def selectSaveFile(self, file="", dir="."):
        return asksaveasfilename(initialfile=file, initialdir=dir)

    def clone(self):
        new = Toplevel()                  # make a new version of me
        myclass = self.__class__          # instance's (lowest) class object
        myclass(new)                      # attach/run instance to new window

    def spawn(self, pycmdline, wait=0):
        if not wait:
            PortableLauncher(pycmdline, pycmdline)()     # run Python progam
        else:
            System(pycmdline, pycmdline)()               # wait for it to exit

    def browser(self, filename):
        new  = Toplevel()                                # make new window
        text = ScrolledText(new, height=30, width=90)    # Text with scrollbar
        text.config(font=('courier', 10, 'normal'))      # use fixed-width font
        text.pack()
        new.title("Text Viewer")                         # set window mgr attrs
        new.iconname("browser")
        text.insert('0.0', open(filename, 'r').read() )  # insert file's text

if __name__ == '__main__':
    class TestMixin(GuiMixin, Frame):      # stand-alone test
        def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.pack()
            Button(self, text='quit',  command=self.quit).pack(fill=X)
            Button(self, text='help',  command=self.help).pack(fill=X)
            Button(self, text='clone', command=self.clone).pack(fill=X)
    TestMixin().mainloop()
