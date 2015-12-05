#!/usr/local/bin/python
from shellgui import *                 # type-specific shell interfaces 
from packdlg  import runPackDialog     # dialogs for data entry
from unpkdlg  import runUnpackDialog   # they both run app classes


class TextPak1(ListMenuGui):
    def __init__(self):
        self.myMenu = [('Pack',    runPackDialog), 
                       ('Unpack',  runUnpackDialog),    # simple functions
                       ('Mtool',   self.notdone)]       # method from guimixin
        ListMenuGui.__init__(self)

    def forToolBar(self, label): 
        return label in ['Pack', 'Unpack']


class TextPak2(DictMenuGui):
    def __init__(self):
        self.myMenu = {'Pack':    runPackDialog,        # or use input here...
                       'Unpack':  runUnpackDialog,      # instead of in dialogs
                       'Mtool':   self.notdone}
        DictMenuGui.__init__(self)


if __name__ == '__main__':                           # self-test code...
    from sys import argv                             # 'menugui.py list|^'
    if len(argv) > 1 and argv[1] == 'list':
        print 'list test'
        TextPak1().mainloop()
    else:
        print 'dict test'
        TextPak2().mainloop()
