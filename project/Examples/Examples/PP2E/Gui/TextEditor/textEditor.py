################################################################################
# PyEdit 1.1: a Python/Tkinter text file editor and component.
# Uses the Tk text widget, plus GuiMaker menus and toolbar buttons
# to implement a full-featured text editor that can be run as a  
# stand-alone program, and attached as a component to other GUIs.
# Also used by PyMail and PyView to edit mail and image file notes.
################################################################################

Version = '1.1'
from Tkinter        import *               # base widgets, constants
from tkFileDialog   import *               # standard dialogs
from tkMessageBox   import *
from tkSimpleDialog import *
from tkColorChooser import askcolor
from string         import split, atoi
from PP2E.Gui.Tools.guimaker import *      # Frame + menu/toolbar builders

START     = '1.0'                          # index of first char: row=1,col=0
SEL_FIRST = SEL + '.first'                 # map sel tag to index
SEL_LAST  = SEL + '.last'                  # same as 'sel.last'

import sys, os, string
FontScale = 0                              # use bigger font on linux
if sys.platform[:3] != 'win':              # and other non-windows boxes
    FontScale = 3

class TextEditor:                          # mix with menu/toolbar Frame class
    startfiledir = '.'
    ftypes = [('All files',     '*'),                 # for file open dialog
              ('Text files',   '.txt'),               # customize in subclass
              ('Python files', '.py')]                # or set in each instance

    colors = [{'fg':'black',      'bg':'white'},      # color pick list
              {'fg':'yellow',     'bg':'black'},      # first item is default
              {'fg':'white',      'bg':'blue'},       # tailor me as desired
              {'fg':'black',      'bg':'beige'},      # or do PickBg/Fg chooser
              {'fg':'yellow',     'bg':'purple'},
              {'fg':'black',      'bg':'brown'},
              {'fg':'lightgreen', 'bg':'darkgreen'},
              {'fg':'darkblue',   'bg':'orange'},
              {'fg':'orange',     'bg':'darkblue'}]

    fonts  = [('courier',    9+FontScale, 'normal'),  # platform-neutral fonts
              ('courier',   12+FontScale, 'normal'),  # (family, size, style)
              ('courier',   10+FontScale, 'bold'),    # or popup a listbox
              ('courier',   10+FontScale, 'italic'),  # make bigger on linux
              ('times',     10+FontScale, 'normal'),
              ('helvetica', 10+FontScale, 'normal'),
              ('ariel',     10+FontScale, 'normal'),
              ('system',    10+FontScale, 'normal'),
              ('courier',   20+FontScale, 'normal')]

    def __init__(self, loadFirst=''):
        if not isinstance(self, GuiMaker):
            raise TypeError, 'TextEditor needs a GuiMaker mixin'
        self.setFileName(None)
        self.lastfind   = None
        self.openDialog = None
        self.saveDialog = None
        self.text.focus()                          # else must click in text
        if loadFirst: 
            self.onOpen(loadFirst)
 
    def start(self):                               # run by GuiMaker.__init__
        self.menuBar = [                           # configure menu/toolbar
            ('File', 0, 
                 [('Open...',    0, self.onOpen),
                  ('Save',       0, self.onSave),
                  ('Save As...', 5, self.onSaveAs),
                  ('New',        0, self.onNew),
                  'separator',
                  ('Quit...',    0, self.onQuit)]
            ),
            ('Edit', 0,
                 [('Cut',        0, self.onCut),
                  ('Copy',       1, self.onCopy),
                  ('Paste',      0, self.onPaste),
                  'separator',
                  ('Delete',     0, self.onDelete),
                  ('Select All', 0, self.onSelectAll)]
            ),
            ('Search', 0,
                 [('Goto...',    0, self.onGoto),
                  ('Find...',    0, self.onFind),
                  ('Refind',     0, self.onRefind),
                  ('Change...',  0, self.onChange)]
            ),
            ('Tools', 0,
                 [('Font List',   0, self.onFontList),
                  ('Pick Bg...',  4, self.onPickBg),
                  ('Pick Fg...',  0, self.onPickFg),
                  ('Color List',  0, self.onColorList),
                 'separator',
                  ('Info...',    0, self.onInfo),
                  ('Clone',      1, self.onClone),
                  ('Run Code',   0, self.onRunCode)]
            )]
        self.toolBar = [
            ('Save',  self.onSave,   {'side': LEFT}),
            ('Cut',   self.onCut,    {'side': LEFT}),
            ('Copy',  self.onCopy,   {'side': LEFT}),
            ('Paste', self.onPaste,  {'side': LEFT}),
            ('Find',  self.onRefind, {'side': LEFT}),
            ('Help',  self.help,     {'side': RIGHT}),
            ('Quit',  self.onQuit,   {'side': RIGHT})]

    def makeWidgets(self):                          # run by GuiMaker.__init__
        name = Label(self, bg='black', fg='white')  # add below menu, above tool
        name.pack(side=TOP, fill=X)                 # menu/toolbars are packed

        vbar  = Scrollbar(self)  
        hbar  = Scrollbar(self, orient='horizontal')
        text  = Text(self, padx=5, wrap='none') 

        vbar.pack(side=RIGHT,  fill=Y)
        hbar.pack(side=BOTTOM, fill=X)                 # pack text last
        text.pack(side=TOP,    fill=BOTH, expand=YES)  # else sbars clipped

        text.config(yscrollcommand=vbar.set)    # call vbar.set on text move
        text.config(xscrollcommand=hbar.set)
        vbar.config(command=text.yview)         # call text.yview on scroll move
        hbar.config(command=text.xview)         # or hbar['command']=text.xview

        text.config(font=self.fonts[0], 
                    bg=self.colors[0]['bg'], fg=self.colors[0]['fg'])
        self.text = text
        self.filelabel = name

    #####################
    # Edit menu commands
    #####################

    def onCopy(self):                           # get text selected by mouse,etc
        if not self.text.tag_ranges(SEL):       # save in cross-app clipboard
            showerror('PyEdit', 'No text selected')
        else:
            text = self.text.get(SEL_FIRST, SEL_LAST)  
            self.clipboard_clear()              
            self.clipboard_append(text)

    def onDelete(self):                         # delete selected text, no save
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.text.delete(SEL_FIRST, SEL_LAST)

    def onCut(self):
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else: 
            self.onCopy()                       # save and delete selected text
            self.onDelete()

    def onPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
        except TclError:
            showerror('PyEdit', 'Nothing to paste')
            return
        self.text.insert(INSERT, text)          # add at current insert cursor
        self.text.tag_remove(SEL, '1.0', END) 
        self.text.tag_add(SEL, INSERT+'-%dc' % len(text), INSERT)
        self.text.see(INSERT)                   # select it, so it can be cut

    def onSelectAll(self):
        self.text.tag_add(SEL, '1.0', END+'-1c')   # select entire text 
        self.text.mark_set(INSERT, '1.0')          # move insert point to top
        self.text.see(INSERT)                      # scroll to top

    ######################
    # Tools menu commands 
    ######################

    def onFontList(self):
        self.fonts.append(self.fonts[0])           # pick next font in list
        del self.fonts[0]                          # resizes the text area
        self.text.config(font=self.fonts[0]) 

    def onColorList(self):
        self.colors.append(self.colors[0])         # pick next color in list
        del self.colors[0]                         # move current to end
        self.text.config(fg=self.colors[0]['fg'], bg=self.colors[0]['bg']) 

    def onPickFg(self): 
        self.pickColor('fg')                       # added on 10/02/00
    def onPickBg(self):                            # select arbitrary color
        self.pickColor('bg')                       # in standard color dialog
    def pickColor(self, part):                     # this is way too easy
        (triple, hexstr) = askcolor()
        if hexstr:
            apply(self.text.config, (), {part: hexstr})

    def onInfo(self):
        text  = self.getAllText()                  # added on 5/3/00 in 15 mins
        bytes = len(text)                          # words uses a simple guess: 
        lines = len(string.split(text, '\n'))      # any separated by whitespace
        words = len(string.split(text)) 
        index = self.text.index(INSERT)
        where = tuple(string.split(index, '.'))
        showinfo('PyEdit Information',
                 'Current location:\n\n' +
                 'line:\t%s\ncolumn:\t%s\n\n' % where +
                 'File text statistics:\n\n' +
                 'bytes:\t%d\nlines:\t%d\nwords:\t%d\n' % (bytes, lines, words))

    def onClone(self):
        new = Toplevel()                # a new edit window in same process
        myclass = self.__class__        # instance's (lowest) class object
        myclass(new)                    # attach/run instance of my class

    def onRunCode(self, parallelmode=1):
        """
        run Python code being edited--not an ide, but handy;
        tries to run in file's dir, not cwd (may be pp2e root);
        inputs and adds command-line arguments for script files;
        code's stdin/out/err = editor's start window, if any;
        but parallelmode uses start to open a dos box for i/o;
        """
        from PP2E.launchmodes import System, Start, Fork
        filemode = 0
        thefile  = str(self.getFileName())
        cmdargs  = askstring('PyEdit', 'Commandline arguments?') or ''
        if os.path.exists(thefile):
            filemode = askyesno('PyEdit', 'Run from file?')
        if not filemode:                                    # run text string
            namespace = {'__name__': '__main__'}            # run as top-level
            sys.argv = [thefile] + string.split(cmdargs)    # could use threads
            exec self.getAllText() + '\n' in namespace      # exceptions ignored
        elif askyesno('PyEdit', 'Text saved in file?'):
            mycwd = os.getcwd()                             # cwd may be root
            os.chdir(os.path.dirname(thefile) or mycwd)     # cd for filenames
            thecmd  = thefile + ' ' + cmdargs
            if not parallelmode:                            # run as file
                System(thecmd, thecmd)()                    # block editor
            else:
                if sys.platform[:3] == 'win':               # spawn in parallel
                    Start(thecmd, thecmd)()                 # or use os.spawnv
                else:
                    Fork(thecmd, thecmd)()                  # spawn in parallel
            os.chdir(mycwd)

    #######################
    # Search menu commands
    #######################
 
    def onGoto(self):
        line = askinteger('PyEdit', 'Enter line number')
        self.text.update() 
        self.text.focus()
        if line is not None:
            maxindex = self.text.index(END+'-1c')
            maxline  = atoi(split(maxindex, '.')[0])
            if line > 0 and line <= maxline:
                self.text.mark_set(INSERT, '%d.0' % line)      # goto line
                self.text.tag_remove(SEL, '1.0', END)          # delete selects
                self.text.tag_add(SEL, INSERT, 'insert + 1l')  # select line
                self.text.see(INSERT)                          # scroll to line
            else:
                showerror('PyEdit', 'Bad line number')

    def onFind(self, lastkey=None):
        key = lastkey or askstring('PyEdit', 'Enter search string')
        self.text.update()
        self.text.focus()
        self.lastfind = key
        if key:
            where = self.text.search(key, INSERT, END)        # don't wrap
            if not where:
                showerror('PyEdit', 'String not found')
            else:
                pastkey = where + '+%dc' % len(key)           # index past key
                self.text.tag_remove(SEL, '1.0', END)         # remove any sel
                self.text.tag_add(SEL, where, pastkey)        # select key 
                self.text.mark_set(INSERT, pastkey)           # for next find
                self.text.see(where)                          # scroll display

    def onRefind(self):
        self.onFind(self.lastfind)

    def onChange(self):
        new = Toplevel(self)
        Label(new, text='Find text:').grid(row=0, column=0)
        Label(new, text='Change to:').grid(row=1, column=0)
        self.change1 = Entry(new)
        self.change2 = Entry(new)
        self.change1.grid(row=0, column=1, sticky=EW)
        self.change2.grid(row=1, column=1, sticky=EW)
        Button(new, text='Find',  
               command=self.onDoFind).grid(row=0, column=2, sticky=EW)
        Button(new, text='Apply', 
               command=self.onDoChange).grid(row=1, column=2, sticky=EW)
        new.columnconfigure(1, weight=1)    # expandable entrys

    def onDoFind(self):
        self.onFind(self.change1.get())                    # Find in change box

    def onDoChange(self):
        if self.text.tag_ranges(SEL):                      # must find first
            self.text.delete(SEL_FIRST, SEL_LAST)          # Apply in change
            self.text.insert(INSERT, self.change2.get())   # deletes if empty
            self.text.see(INSERT)
            self.onFind(self.change1.get())                # goto next appear
            self.text.update()                             # force refresh

    #####################
    # File menu commands
    #####################

    def my_askopenfilename(self):      # objects remember last result dir/file
        if not self.openDialog:
           self.openDialog = Open(initialdir=self.startfiledir, 
                                  filetypes=self.ftypes)
        return self.openDialog.show()

    def my_asksaveasfilename(self):    # objects remember last result dir/file
        if not self.saveDialog:
           self.saveDialog = SaveAs(initialdir=self.startfiledir, 
                                    filetypes=self.ftypes)
        return self.saveDialog.show()
        
    def onOpen(self, loadFirst=''):
        doit = self.isEmpty() or askyesno('PyEdit', 'Disgard text?')
        if doit:
            file = loadFirst or self.my_askopenfilename()
            if file:
                try:
                    text = open(file, 'r').read()
                except:
                    showerror('PyEdit', 'Could not open file ' + file)
                else:
                    self.setAllText(text)
                    self.setFileName(file)

    def onSave(self):
        self.onSaveAs(self.currfile)  # may be None

    def onSaveAs(self, forcefile=None):
        file = forcefile or self.my_asksaveasfilename()
        if file:
            text = self.getAllText()
            try:
                open(file, 'w').write(text)
            except:
                showerror('PyEdit', 'Could not write file ' + file)
            else:
                self.setFileName(file)         # may be newly created

    def onNew(self):
        doit = self.isEmpty() or askyesno('PyEdit', 'Disgard text?')
        if doit:
            self.setFileName(None)
            self.clearAllText()

    def onQuit(self):
        if askyesno('PyEdit', 'Really quit PyEdit?'):
            self.quit()                        # Frame.quit via GuiMaker

    ####################################
    # Others, useful outside this class
    ####################################

    def isEmpty(self):
        return not self.getAllText() 

    def getAllText(self):
        return self.text.get('1.0', END+'-1c')  # extract text as a string

    def setAllText(self, text):
        self.text.delete('1.0', END)            # store text string in widget
        self.text.insert(END, text)             # or '1.0'
        self.text.mark_set(INSERT, '1.0')       # move insert point to top 
        self.text.see(INSERT)                   # scroll to top, insert set

    def clearAllText(self):
        self.text.delete('1.0', END)            # clear text in widget 

    def getFileName(self):
        return self.currfile

    def setFileName(self, name):
        self.currfile = name  # for save
        self.filelabel.config(text=str(name))

    def help(self):
        showinfo('About PyEdit', 
                 'PyEdit version %s\nOctober, 2000\n\n'
                 'A text editor program\nand object component\n'
                 'written in Python/Tk.\nProgramming Python 2E\n'
                 "O'Reilly & Associates" % Version)


##################################################################
# ready-to-use editor classes 
# mix in a Frame subclass that builds menu/toolbars
##################################################################


# when editor owns the window 

class TextEditorMain(TextEditor, GuiMakerWindowMenu):  # add menu/toolbar maker 
    def __init__(self, parent=None, loadFirst=''):     # when fills whole window
        GuiMaker.__init__(self, parent)                # use main window menus
        TextEditor.__init__(self, loadFirst)           # self has GuiMaker frame
        self.master.title('PyEdit ' + Version)         # title iff stand alone
        self.master.iconname('PyEdit')                 # catch wm delete button
        self.master.protocol('WM_DELETE_WINDOW', self.onQuit)

class TextEditorMainPopup(TextEditor, GuiMakerWindowMenu):
    def __init__(self, parent=None, loadFirst=''):     
        self.popup = Toplevel(parent)                  # create own window
        GuiMaker.__init__(self, self.popup)            # use main window menus
        TextEditor.__init__(self, loadFirst) 
        assert self.master == self.popup
        self.popup.title('PyEdit ' + Version) 
        self.popup.iconname('PyEdit')               
    def quit(self):
        self.popup.destroy()                           # kill this window only


# when embedded in another window

class TextEditorComponent(TextEditor, GuiMakerFrameMenu):     
    def __init__(self, parent=None, loadFirst=''):     # use Frame-based menus
        GuiMaker.__init__(self, parent)                # all menus, buttons on
        TextEditor.__init__(self, loadFirst)           # GuiMaker must init 1st

class TextEditorComponentMinimal(TextEditor, GuiMakerFrameMenu): 
    def __init__(self, parent=None, loadFirst='', deleteFile=1):   
        self.deleteFile = deleteFile
        GuiMaker.__init__(self, parent)             
        TextEditor.__init__(self, loadFirst) 
    def start(self):   
        TextEditor.start(self)                         # GuiMaker start call
        for i in range(len(self.toolBar)):             # delete quit in toolbar
            if self.toolBar[i][0] == 'Quit':           # delete file menu items
                del self.toolBar[i]; break             # or just disable file
        if self.deleteFile:
            for i in range(len(self.menuBar)):
                if self.menuBar[i][0] == 'File':
                    del self.menuBar[i]; break
        else:
            for (name, key, items) in self.menuBar:
                if name == 'File':
                    items.append([1,2,3,4,6]) 


# stand-alone program run
                                                     
def testPopup():     
    # see PyView and PyMail for component tests
    root = Tk()
    TextEditorMainPopup(root)
    TextEditorMainPopup(root)
    Button(root, text='More', command=TextEditorMainPopup).pack(fill=X)
    Button(root, text='Quit', command=root.quit).pack(fill=X)
    root.mainloop()

def main():                                           # may be typed or clicked
    try:                                              # or associated on Windows
        fname = sys.argv[1]                           # arg = optional filename
    except IndexError:
        fname = None
    TextEditorMain(loadFirst=fname).pack(expand=YES, fill=BOTH)
    mainloop()

if __name__ == '__main__':                            # when run as a script
    #testPopup()
    main()                                            # run .pyw for no dos box
