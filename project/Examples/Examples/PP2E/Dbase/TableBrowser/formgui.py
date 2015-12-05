#!/usr/local/bin/python
#############################################################################
# PyForm: a persistent table viewer GUI. Uses guimixin for std dialogs.
# Assumes the browsed table has a dictionary-of-dictionary interface, and
# relies on table wrapper classes to convert other structures as needed.
# Store an initial record with dbinit script to start a dbase from scratch.
# Caveat: doesn't do object method calls, shows complex field values poorly.
#############################################################################

from Tkinter  import *                                 # Tk widgets
from guitools import frame, label, button, entry       # widget builders
from PP2E.Gui.Tools.guimixin import GuiMixin           # common methods

class FormGui(GuiMixin, Frame):
    def __init__(self, mapping):                       # an extended frame
        Frame.__init__(self)                           # on default top-level
        self.pack(expand=YES, fill=BOTH)               # all parts expandable
        self.master.title('PyForm 2.0 - Table browser')       
        self.master.iconname("PyForm")
        self.makeMainBox()
        self.table     = mapping               # a dict, dbm, shelve, Table,..
        self.index     = mapping.keys()        # list of table keys
        self.cursor    = -1                    # current index position
        self.currslots = []                    # current form's (key,text)'s
        self.currform  = None                  # current form window
        self.listbox   = None                  # index listbox window

    def makeMainBox(self):
        frm = frame(self, TOP)
        frm.config(bd=2)
        button(frm, LEFT, 'next',  self.onNext)       # next in list
        button(frm, LEFT, 'prev',  self.onPrev)       # backup in list
        button(frm, LEFT, 'find',  self.onFind)       # find from key
        frm = frame(self, TOP)
        self.keytext = StringVar()                    # current record's key
        label(frm, LEFT, 'KEY=>')                     # change before 'find'
        entry(frm, LEFT,  self.keytext)             
        frm = frame(self, TOP)
        frm.config(bd=2)
        button(frm,  LEFT,  'store',  self.onStore)     # updated entry data
        button(frm,  LEFT,  'new',    self.onNew)       # clear fields
        button(frm,  LEFT,  'index',  self.onMakeList)  # show key list
        button(frm,  LEFT,  'delete', self.onDelete)    # show key list
        button(self, BOTTOM,'quit',   self.quit)        # from guimixin

    def onPrev(self):
        if self.cursor <= 0:
            self.infobox('Backup', "Front of table")
        else:
            self.cursor = self.cursor - 1
            self.display()

    def onNext(self):
        if self.cursor >= len(self.index)-1:
            self.infobox('Advance', "End of table")
        else:
            self.cursor = self.cursor + 1
            self.display()

    def sameKeys(self, record):                 # can we reuse the same form?
        keys1 = record.keys()
        keys2 = map(lambda x:x[0], self.currslots)
        keys1.sort(); keys2.sort()              # keys list order differs
        return keys1 == keys2                   # if insertion-order differs

    def display(self):
        key = self.index[self.cursor]           # show record at index cursor
        self.keytext.set(key)                   # change key in main box 
        record = self.table[key]                # in dict, dbm, shelf, class
        if self.sameKeys(record): 
            self.currform.title('PyForm - Key=' + `key`)  
            for (field, text) in self.currslots:
                text.set(`record[field]`)       # same fields? reuse form
        else:                                   # expr `x` works like repr(x)
            if self.currform:
                self.currform.destroy()         # different fields?  
            new = Toplevel()                    # replace current box
            new.title('PyForm - Key=' + `key`)  # new resizable window
            new.iconname("pform")
            left  = frame(new, LEFT)
            right = frame(new, RIGHT)
            self.currslots = []                 # list of (field, entry)
            for field in record.keys():
                label(left, TOP, `field`)       # key,value to strings
                text = StringVar()              # we could sort keys here
                text.set( `record[field]` )
                entry(right, TOP, text, width=40)
                self.currslots.append((field, text))
            self.currform = new
            new.protocol('WM_DELETE_WINDOW', lambda:0)   # ignore destroy's
        self.selectlist()                                # update listbox

    def onStore(self):
        if not self.currform: return
        key = self.keytext.get()
        if key in self.index:                    # change existing record
            record = self.table[key]             # not: self.table[key][field]=
        else:
            record = {}                          # create a new record
            self.index.append(key)               # add to index and listbox
            if self.listbox:
                self.listbox.insert(END, key)    # or at len(self.index)-1 
        for (field, text) in self.currslots:
            try:                                 # fill out dictionary rec
                record[field] = eval(text.get()) # convert back from string
            except:
                self.errorbox('Bad data: "%s" = "%s"' % (field, text.get()))
                record[field] = None
        self.table[key] = record                 # add to dict, dbm, shelf,...
        self.onFind(key)                         # readback: set cursor,listbox

    def onNew(self):
        if not self.currform: return               # clear input form and key
        self.keytext.set('?%d' % len(self.index))  # default key unless typed
        for (field, text) in self.currslots:       # clear key/fields for entry
            text.set('') 
        self.currform.title('Key: ?')  
 
    def onFind(self, key=None):
        target = key or self.keytext.get()            # passed in, or entered
        try:
            self.cursor = self.index.index(target)    # find label in keys list
            self.display()
        except:
            self.infobox('Not found', "Key doesn't exist", 'info')

    def onDelete(self):
        if not self.currform or not self.index: return
        currkey = self.index[self.cursor]
        del self.table[currkey]                      # table, index, listbox
        del self.index[self.cursor:self.cursor+1]    # like "list[i:i+1] = []"
        if self.listbox: 
            self.listbox.delete(self.cursor)         # delete from listbox 
        if self.cursor < len(self.index):
            self.display()                           # show next record if any 
        elif self.cursor > 0:
            self.cursor = self.cursor-1              # show prior if delete end
            self.display()
        else:                                        # leave box if delete last
            self.onNew() 

    def onList(self,evnt):
        if not self.index: return                  # on listbox double-click
        index = self.listbox.curselection()        # fetch selected key text
        label = self.listbox.get(index)            # or use listbox.get(ACTIVE)
        self.onFind(label)                         # and call method here

    def onMakeList(self):
        if self.listbox: return                    # already up?
        new = Toplevel()                           # new resizable window
        new.title("PyForm - Key Index")            # select keys from a listbox
        new.iconname("pindex")
        frm    = frame(new, TOP)
        scroll = Scrollbar(frm)
        list   = Listbox(frm, bg='white')
        scroll.config(command=list.yview, relief=SUNKEN)
        list.config(yscrollcommand=scroll.set, relief=SUNKEN)
        scroll.pack(side=RIGHT, fill=BOTH)
        list.pack(side=LEFT, expand=YES, fill=BOTH)    # pack last, clip first
        for key in self.index:                         # add to list-box
            list.insert(END, key)                      # or: sort list first
        list.config(selectmode=SINGLE, setgrid=1)      # select,resize modes
        list.bind('<Double-1>', self.onList)           # on double-clicks
        self.listbox = list
        if self.index and self.cursor >= 0:            # highlight position
            self.selectlist()
        new.protocol('WM_DELETE_WINDOW', lambda:0)     # ignore destroy's

    def selectlist(self):                              # listbox tracks cursor
        if self.listbox:         
            self.listbox.select_clear(0, self.listbox.size())
            self.listbox.select_set(self.cursor)

if __name__ == '__main__': 
    from PP2E.Dbase.testdata import cast        # self-test code
    for k in cast.keys(): print k, cast[k]      # view in-memory dict-of-dicts
    FormGui(cast).mainloop()
    for k in cast.keys(): print k, cast[k]      # show modified table on exit
