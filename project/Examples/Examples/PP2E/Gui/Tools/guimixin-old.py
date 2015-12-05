#####################################################
# a "mixin" class for other frames 
# common methods for canned-dialogs, spawning, etc.
# must be mixed with a class derived from Frame
#####################################################

# use tkSimpleDialogs for info, warn, etc.
# fix demo path???, or split off into demo module
# make browser text fixed-width font


PDIR = '/home/mark/python-1.3/Python-1.3'    # path to 'python' for demos

from Tkinter import *
from Dialog import Dialog
from ScrolledText import ScrolledText

class GuiMixin:
    def question(self, title, text, bitmap='question', strings=('Yes', 'No')):
        return Dialog(self, 
                      title  = title, 
                      text   = text, 
                      bitmap = bitmap, 
                      default= 1, strings=strings).num

    def infobox(self, title, text, bitmap='', strings=('OK',)):
        Dialog(self, 
            title=title, text=text, bitmap=bitmap, default=0, strings=strings)

    def quit(self):
        ans = self.question('Verify quit', 'Are you sure you want to quit?')
        if ans == 0: 
            Frame.quit(self)

    def notdone(self):
        self.infobox('Not implemented', 'Option not available', 'error')

    def help(self):
        self.infobox('RTFM', 'See figure 1...', 'info')   # override this

    def errorbox(self, text):
        self.infobox('Error!', text, 'error')

    def clone(self):
        new = Toplevel()               # make a new version of me
        myclass = self.__class__       # instance's (lowest) class object
        myclass(new)                   # attach/run instance of my class

    def spawn(self, demo, fork=0):
        import os                                # run /Demo program by name
        try:
            pbase = os.environ['PYTHONBASE']     # env var overrides
        except:
            pbase = PDIR
        python = pbase + '/python'
        if not fork:
            os.system('%s %s/Demo/tkinter/%s' % (python, pbase, demo) ) 
        else:
            pid = os.fork()
            if pid == 0:
                os.execv(python, (python, pbase+'/Demo/tkinter/'+demo))

    def browser(self, file):
        new  = Toplevel()
        text = ScrolledText(new, height=30, width=90)
        text.config(font=('Courier', 9, 'normal'))
        text.pack()
        new.title("Poor-man's Text Editor")
        new.iconname("PyBrowser")
        text.insert('0.0', open(file, 'r').read() )


if __name__ == '__main__':
    class TestMixin(GuiMixin, Frame):           # stand-alone test
        def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.pack()
            Button(self, text='quit',  command=self.quit).pack(fill=X)
            Button(self, text='help',  command=self.help).pack(fill=X)
            Button(self, text='clone', command=self.clone).pack(fill=X)
    TestMixin().mainloop()
