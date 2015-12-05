# 2/00: wrap note file save in try so doesn't fail if run off cd;
#       add note about threads and PyMailGui
#
# MENTION: idle path browser -> Tkinter.py; Tcl/Tk parms books
# note: can't map back from image to self.files list from initial
# glob--may open file anywhere, in open dialog (not on glob list)
# mention ipwp for internet topics
# after works as good as threads here (uses threads)
# + show top menu varient
# disable file menu for component (TextEditor)
# note: superclass's makeWidgets hasn't set self.msecs 
# yet in overloaded makeWidgets here (later in constructor)
# note: from canvaspicsthreads import SlideShow -> fails, 
# because doesn't call overloadable method each time, so
# changed canvaspics to have common drawNext method
#
# thread bug and locks: when close note box by pressing 'Note',
# it's possible that the timer thread may be in the midst of a
# drawNext call: drawNext->switchNote->saveNote->editor.getAllText
# ->text.get('1.0',...); when it starts saveNote the editor is
# open, but by the time it gets to the text widget operation,
# the text widget may have been destroyed as the result of the 
# onNote callback handler execution (the thread runs in parallel
# with the callback handler);  to prevent this, a lock is used 
# to prevent saveNote from running is a destroy is in progress;
# the thread module's allocate_lock returns a lock object, which
# is sometimes called a mutex or binary semaphore; lock objects
# may be acquired by at most one thread at a given time; they 
# start unlocked,and is used to synchronize (serialize) the thread
# and callback handler;  this isn't an issue if we use the Tk
# after to do the timer, but threads can be faster in general...
#     see PyMailGui: only main thread can do GUI updates/ops
##################################################################


import os, string, thread
from Tkinter import *
from PP2E.Gui.TextEditor.textEditor import *
from slideShow_threads import SlideShow

class SlideShowPlus(SlideShow):
    def __init__(self, parent, picdir, editclass, msecs=2000):
        self.msecs = msecs
        self.editclass = editclass
        self.destroyer = thread.allocate_lock()
        SlideShow.__init__(self, parent=parent, picdir=picdir, msecs=msecs)
    def makeWidgets(self):
        self.name = Label(self, text='None', bg='red', relief=RIDGE)
        self.name.pack(fill=X)
        SlideShow.makeWidgets(self)
        Button(self, text='Note', command=self.onNote).pack(fill=BOTH)
        s = Scale(label='Speed: msec delay', command=self.onScale, 
                  from_=0, to=3000, resolution=50, showvalue=YES,
                  length=400, tickinterval=250, orient='horizontal')
        s.pack(side=BOTTOM, fill=X, expand=YES)
        s.set(self.msecs)
        self.editor = self.image = None
    def onStart(self):
        SlideShow.onStart(self)
        self.config(cursor='watch')
    def onStop(self):
        SlideShow.onStop(self)
        self.config(cursor='hand2')
    def onOpen(self):
        SlideShow.onOpen(self)
        if self.image: 
            self.name.config(text=os.path.split(self.image[0])[1])
        self.config(cursor='crosshair')
        self.switchNote()
    def onQuit(self):
        self.saveNote()
        SlideShow.onQuit(self)
    def drawNext(self):
        SlideShow.drawNext(self)
        if self.image: 
            self.name.config(text=os.path.split(self.image[0])[1])
        self.destroyer.acquire()
        self.switchNote()                         # don't let editor go away
        self.destroyer.release()
    def onScale(self, value):
        self.msecs = string.atoi(value)
    def onNote(self):
        if self.editor:                           # if editor already open 
            self.destroyer.acquire()              # save text, delete editor
            self.saveNote() 
            self.editor.destroy()                 # serialize the destroy 
            self.editor = None
            self.destroyer.release()
        else:                                           # else create editor
            if self.editclass == TextEditorMain:        # and load note text
                win = Toplevel() 
                self.editor = TextEditorMain(win)       # new popup window
                self.editor.pack(side=TOP) 
            else:
                self.editor = self.editclass(self)      # embedded in self
                self.editor.pack(side=TOP)
            self.loadNote()
    def switchNote(self):
        if self.editor:
            self.saveNote()       # save current image's note
            self.loadNote()       # load note for new image
    def saveNote(self):
        if self.editor:
            currfile = self.editor.getFileName()
            currtext = self.editor.getAllText()
            if currfile and currtext:
                try:
                    open(currfile, 'w').write(currtext)
                except:
                    pass # may be normal if run off cd
    def loadNote(self):
        if self.image:
            root, ext = os.path.splitext(self.image[0])
            notefile  = root + '.note'
            self.editor.setFileName(notefile)
            try:
                self.editor.setAllText(open(notefile).read())
            except:
                self.editor.clearAllText()

if __name__ == '__main__':
    import sys
    editstyle = TextEditorComponentMinimal
    if len(sys.argv) >= 2:
        try:
            editstyle = [TextEditorMain,
                         TextEditorComponent,
                         TextEditorComponentMinimal][string.atoi(sys.argv[1])]
        except: pass
    picdir = '../gifs'
    if len(sys.argv) == 3:
        picdir = sys.argv[2]

    root = Tk()
    root.title('PyView 1.1, plus text notes - threads test')
    Label(root, text="Slide show subclass").pack()
    SlideShowPlus(parent=root, picdir=picdir, editclass=editstyle).pack()
    root.mainloop()
