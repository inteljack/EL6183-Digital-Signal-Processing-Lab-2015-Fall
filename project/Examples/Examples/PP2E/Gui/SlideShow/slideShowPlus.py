###################################################################
# SlideShowPlus: add note files with an attached PyEdit object,
# a scale for setting the slideshow delay interval, and a label
# that gives the name of the image file currently being displayed;
###################################################################

import os, string
from Tkinter import *
from PP2E.Gui.TextEditor.textEditor import *
from slideShow import SlideShow
#from slideShow_threads import SlideShow

class SlideShowPlus(SlideShow):
    def __init__(self, parent, picdir, editclass, msecs=2000):
        self.msecs = msecs
        self.editclass = editclass
        SlideShow.__init__(self, parent=parent, picdir=picdir, msecs=msecs)
    def makeWidgets(self):
        self.name = Label(self, text='None', bg='red', relief=RIDGE)
        self.name.pack(fill=X)
        SlideShow.makeWidgets(self)
        Button(self, text='Note', command=self.onNote).pack(fill=X)
        Button(self, text='Help', command=self.onHelp).pack(fill=X)
        s = Scale(label='Speed: msec delay', command=self.onScale, 
                  from_=0, to=3000, resolution=50, showvalue=YES,
                  length=400, tickinterval=250, orient='horizontal')
        s.pack(side=BOTTOM, fill=X)
        s.set(self.msecs)
        if self.editclass == TextEditorMain:          # make editor now
            self.editor = self.editclass(self.master) # need root for menu
        else:
            self.editor = self.editclass(self)        # embedded or popup
        self.editor.pack_forget()                     # hide editor initially
        self.editorUp = self.image = None
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
    def quit(self):
        self.saveNote()
        SlideShow.quit(self)
    def drawNext(self):
        SlideShow.drawNext(self)
        if self.image: 
            self.name.config(text=os.path.split(self.image[0])[1])
        self.loadNote() 
    def onScale(self, value):
        self.msecs = string.atoi(value)
    def onNote(self):
        if self.editorUp:                  # if editor already open 
            #self.saveNote()               # save text, hide editor
            self.editor.pack_forget() 
            self.editorUp = 0
        else:
            self.editor.pack(side=TOP)     # else unhide/pack editor
            self.editorUp = 1              # and load image note text
            self.loadNote()
    def switchNote(self):
        if self.editorUp:
            self.saveNote()                # save current image's note
            self.loadNote()                # load note for new image
    def saveNote(self):
        if self.editorUp:
            currfile = self.editor.getFileName()     # or self.editor.onSave()
            currtext = self.editor.getAllText()      # but text may be empty
            if currfile and currtext:
                try:
                    open(currfile, 'w').write(currtext)
                except:
                    pass # this may be normal if run off cd
    def loadNote(self):
        if self.image and self.editorUp:
            root, ext = os.path.splitext(self.image[0])
            notefile  = root + '.note'
            self.editor.setFileName(notefile)
            try:
                self.editor.setAllText(open(notefile).read())
            except:
                self.editor.clearAllText()
    def onHelp(self):
        showinfo('About PyView',
                 'PyView version 1.1\nJuly, 1999\n'
                 'An image slide show\nProgramming Python 2E')

if __name__ == '__main__':
    import sys
    picdir = '../gifs'
    if len(sys.argv) >= 2:
        picdir = sys.argv[1]

    editstyle = TextEditorComponentMinimal
    if len(sys.argv) == 3:
        try:
            editstyle = [TextEditorMain,
                         TextEditorMainPopup,
                         TextEditorComponent,
                         TextEditorComponentMinimal][string.atoi(sys.argv[2])]
        except: pass

    root = Tk()
    root.title('PyView 1.1 - plus text notes')
    Label(root, text="Slide show subclass").pack()
    SlideShowPlus(parent=root, picdir=picdir, editclass=editstyle)
    root.mainloop()
