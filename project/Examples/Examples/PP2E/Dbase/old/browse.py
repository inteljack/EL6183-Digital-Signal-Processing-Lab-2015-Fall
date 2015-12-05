#!/usr/local/bin/python
from TableBrowser.formgui import FormGui
from formtbl2 import *
from person   import Person
FormGui(ClassTable(Person, ShelveTable(None,'data/folks'))).mainloop()
