import shelve
from TableBrowser.formgui import FormGui    # after initcast
db = shelve.open('data/castfile')           # reopen shelve file
FormGui(db).mainloop()                      # browse existing shelve-of-dicts
