#########################################################
# search for demos shipped in Python source distribution;
# PATH and PP2EHOME won't help here, because these demos 
# are not part of the standard install or the book's tree
######################################################### 

import os, string, PP2E.Launcher
demoDir  = None
myTryDir = ''

#sourceDir = r'C:\Stuff\Etc\Python-ddj-cd\distributions'
#myTryDir  = sourceDir + r'\Python-1.5.2\Demo\tkinter'

def findDemoDir():
    global demoDir
    if not demoDir:                        # only searches on first call
        if os.path.exists(myTryDir):       # use hard-coded dir, or search
            demoDir = myTryDir             # save in global for next call 
        else:
            print 'Searching for standard demos on your machine...'
            path = PP2E.Launcher.guessLocation('hanoi.py')
            if path:
                demoDir = string.join(string.split(path, os.sep)[:-2], os.sep)
                print 'Using demo dir:', demoDir
    assert demoDir, 'Where is your demo directory?'
    return demoDir
