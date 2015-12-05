#!/usr/local/bin/python
from shellgui import *       # type-specific shell interfaces 

class TextPak1(ListMenuGui):
    def __init__(self):
        self.myMenu = [('Pack',    self.Pack), 
                       ('Unpack',  self.Unpack),
                       ('Mtool',   self.Missing)]
        ListMenuGui.__init__(self)

    def forToolBar(self, label): 
        return label in ['Pack', 'Unpack']

    def Pack(self):    print 'pack dialog...'
    def Unpack(self):  print 'unpack dialog...'
    def Missing(self): print 'not yet implemented...'

class TextPak2(DictMenuGui):
    def __init__(self):
        self.myMenu = {'Pack':    self.Pack, 
                       'Unpack':  self.Unpack,
                       'Mtool':   self.Missing}
        DictMenuGui.__init__(self)

    def Pack(self):    print 'pack dialog...'
    def Unpack(self):  print 'unpack dialog...'
    def Missing(self): print 'not yet implemented...'

if __name__ == '__main__':               # self-test code...
    from sys import argv
    if len(argv) > 1 and argv[1] == 'list':
        print 'list test'
        TextPak1().mainloop()
    else:
        print 'dict test'
        TextPak2().mainloop()
