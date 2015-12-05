# use composition, not inheritance

from Tkinter import * 
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename
from quitter        import Quitter
from scrolledtext   import ScrolledText                  

class SimpleEditor(Frame):    
    def __init__(self, parent=None, file=None): 
        Frame.__init__(self, parent)
        self.pack()
        frm = Frame(self)
        frm.pack(fill=X)
        Button(frm, text='Save',  command=self.onSave).pack(side=LEFT)
        Button(frm, text='Cut',   command=self.onCut).pack(side=LEFT)
        Button(frm, text='Paste', command=self.onPaste).pack(side=LEFT)
        Button(frm, text='Find',  command=self.onFind).pack(side=LEFT)
        Quitter(frm).pack(side=LEFT)
        self.st = ScrolledText(self, file=file)           # attach, not subclass
        self.st.text.config(font=('courier', 9, 'normal'))
    def onSave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.st.text.get('1.0', END+'-1c')  # go through attribute
            open(filename, 'w').write(alltext)          
    def onCut(self):
        text = self.st.text.get(SEL_FIRST, SEL_LAST)   
        self.st.text.delete(SEL_FIRST, SEL_LAST) 
        self.clipboard_clear()              
        self.clipboard_append(text)
    def onPaste(self):                                   
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.st.text.insert(INSERT, text)
        except TclError:
            pass                                          
    def onFind(self):
        target = askstring('SimpleEditor', 'Search String?')
        if target:
            where = self.st.text.search(target, INSERT, END) 
            if where:   
                print where
                pastit = where + ('+%dc' % len(target))   
               #self.st.text.tag_remove(SEL, '1.0', END) 
                self.st.text.tag_add(SEL, where, pastit)   
                self.st.text.mark_set(INSERT, pastit)     
                self.st.text.see(INSERT)                 
                self.st.text.focus()                    

if __name__ == '__main__':
    try:
        SimpleEditor(file=sys.argv[1]).mainloop()    # filename on command line
    except IndexError:
        SimpleEditor().mainloop()                    # or not

