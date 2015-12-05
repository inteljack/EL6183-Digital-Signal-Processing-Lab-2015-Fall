editor = 'vi'  # your editor's name

def python(cmd):
    import __main__
    exec cmd in __main__.__dict__, __main__.__dict__

def edit(filename):
    import os
    os.system(editor + ' ' + filename)

def fix(modname):                            
    import sys                              # ex: fix('textpak4')
    edit(modname + '.py')                   # assumes in '.'
    if modname in sys.modules.keys():
        python('reload(' + modname + ')')   # reload in __main__
    else:
        python('import ' + modname)         # first load in __main__
