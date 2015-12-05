#!/usr/bin/env python
"""
----------------------------------------------------------------------------
Tools to find files, and run Python demos even if your environment has
not been manually configured yet.  For instance, provided you have already
installed Python, you can launch Tk demos directly off the book's CD by 
double-clicking this file's icon, without first changing your environment
config files.  Assumes Python has been installed first (double-click on the
python self-install exe on the CD), and tries to guess where Python and the 
examples distribution live on your machine.  Sets Python module and system
search paths before running scripts: this only works because env settings 
are inherited by spawned programs on both windows and linux.  You may want
to tweak the list of directories searched for speed, and probably want to 
run one of the Config/setup-pp files at startup time to avoid this search.
This script is friendly to already-configured path settings, and serves to 
demo platform-independent directory path processing.  Python programs can 
always be started under the Windows port by clicking (or spawning a 'start'
DOS command), but many book examples require the module search path too.
----------------------------------------------------------------------------
"""

import sys, os, string


def which(program, trace=1):
    """
    Look for program in all dirs in the system's search 
    path var, PATH; return full path to program if found, 
    else None. Doesn't handle aliases on Unix (where we 
    could also just run a 'which' shell cmd with os.popen),
    and it might help to also check if the file is really 
    an executable with os.stat and the stat module, using
    code like this: os.stat(filename)[stat.ST_MODE] & 0111
    """
    try:
        ospath = os.environ['PATH']
    except:
        ospath = '' # okay if not set
    systempath = string.split(ospath, os.pathsep)
    if trace: print 'Looking for', program, 'on', systempath
    for sysdir in systempath:
        filename = os.path.join(sysdir, program)      # adds os.sep between
        if os.path.isfile(filename):                  # exists and is a file?
            if trace: print 'Found', filename
            return filename
        else:
            if trace: print 'Not at', filename
    if trace: print program, 'not on system path'
    return None


def findFirst(thisDir, targetFile, trace=0):    
    """
    Search directories at and below thisDir for a file
    or dir named targetFile.  Like find.find in standard
    lib, but no name patterns, follows unix links, and
    stops at the first file found with a matching name.
    targetFile must be a simple base name, not dir path.
    """
    if trace: print 'Scanning', thisDir
    for filename in os.listdir(thisDir):                    # skip . and ..
        if filename in [os.curdir, os.pardir]:              # just in case
            continue
        elif filename == targetFile:                        # check name match
            return os.path.join(thisDir, targetFile)        # stop at this one
        else: 
            pathname = os.path.join(thisDir, filename)      # recur in subdirs
            if os.path.isdir(pathname):                     # stop at 1st match
                below = findFirst(pathname, targetFile, trace)  
                if below: return below

       
def guessLocation(file, isOnWindows=(sys.platform[:3]=='win'), trace=1):
    """
    Try to find directory where file is installed
    by looking in standard places for the platform.
    Change tries lists as needed for your machine.
    """
    cwd = os.getcwd()                             # directory where py started
    tryhere = cwd + os.sep + file                 # or os.path.join(cwd, file)
    if os.path.exists(tryhere):                   # don't search if it is here
        return tryhere                            # findFirst(cwd,file) descends
    if isOnWindows:
        tries = []
        for pydir in [r'C:\Python20', r'C:\Program Files\Python']:
            if os.path.exists(pydir):
                tries.append(pydir)
        tries = tries + [cwd, r'C:\Program Files']
        for drive in 'CGDEF':
            tries.append(drive + ':\\')
    else:
        tries = [cwd, os.environ['HOME'], '/usr/bin', '/usr/local/bin']
    for dir in tries:
        if trace: print 'Searching for %s in %s' % (file, dir)
        try:
            match = findFirst(dir, file)
        except OSError: 
            if trace: print 'Error while searching', dir     # skip bad drives
        else:
            if match: return match
    if trace: print file, 'not found! - configure your environment manually'
    return None


PP2EpackageRoots = [                               # python module search path
   #'%sPP2E' % os.sep,                             # pass in your own elsewhere
    '']                                            # '' adds examplesDir root


def configPythonPath(examplesDir, packageRoots=PP2EpackageRoots, trace=1):
    """
    Setup the Python module import search-path directory 
    list as necessary to run programs in the book examples 
    distribution, in case it hasn't been configured already.
    Add examples package root, plus nested package roots.
    This corresponds to the setup-pp* config file settings.
    os.environ assignments call os.putenv internally in 1.5,
    so these settings will be inherited by spawned programs.
    Python source lib dir and '.' are automatically searched;
    unix|win os.sep is '/' | '\\', os.pathsep is ':' | ';'.
    sys.path is for this process only--must set os.environ.
    adds new dirs to front, in case there are two installs.
    could also try to run platform's setup-pp* file in this
    process, but that's non-portable, slow, and error-prone.
    """
    try:
        ospythonpath = os.environ['PYTHONPATH']
    except:
        ospythonpath = '' # okay if not set 
    if trace: print 'PYTHONPATH start:\n', ospythonpath
    addList = []
    for root in packageRoots:
        importDir = examplesDir + root
        if importDir in sys.path:
            if trace: print 'Exists', importDir
        else:
            if trace: print 'Adding', importDir
            sys.path.append(importDir)
            addList.append(importDir)
    if addList:
        addString = string.join(addList, os.pathsep) + os.pathsep
        os.environ['PYTHONPATH'] = addString + ospythonpath
        if trace: print 'PYTHONPATH updated:\n', os.environ['PYTHONPATH']
    else:
        if trace: print 'PYTHONPATH unchanged'


def configSystemPath(pythonDir, trace=1):
    """ 
    Add python executable dir to system search path if needed
    """
    try:
        ospath = os.environ['PATH']
    except:
        ospath = '' # okay if not set  
    if trace: print 'PATH start', ospath
    if (string.find(ospath, pythonDir) == -1 and                # not found?
        string.find(ospath, string.upper(pythonDir)) == -1):    # case diff?
        os.environ['PATH'] = ospath + os.pathsep + pythonDir
        if trace: print 'PATH updated:', os.environ['PATH']
    else:
        if trace: print 'PATH unchanged'


def runCommandLine(pypath, exdir, command, isOnWindows=0, trace=1):
    """
    Run python command as an independent program/process on 
    this platform, using pypath as the Python executable,
    and exdir as the installed examples root directory.
    Need full path to python on windows, but not on unix.
    On windows, a os.system('start ' + command) is similar,
    except that .py files pop up a dos console box for i/o.
    Could use launchmodes.py too but pypath is already known. 
    """
    command = exdir + os.sep + command          # rooted in examples tree
    os.environ['PP2E_PYTHON_FILE'] = pypath     # export directories for
    os.environ['PP2E_EXAMPLE_DIR'] = exdir      # use in spawned programs

    if trace: print 'Spawning:', command
    if isOnWindows:
        os.spawnv(os.P_DETACH, pypath, ('python', command))
    else:
        cmdargs = [pypath] + string.split(command)
        if os.fork() == 0:
            os.execv(pypath, cmdargs)           # run prog in child process


def launchBookExamples(commandsToStart, trace=1):
    """
    Toplevel entry point: find python exe and 
    examples dir, config env, spawn programs
    """
    isOnWindows  = (sys.platform[:3] == 'win')
    pythonFile   = (isOnWindows and 'python.exe') or 'python'
    examplesFile = 'README-PP2E.txt'
    if trace: 
        print os.getcwd(), os.curdir, os.sep, os.pathsep
        print 'starting on %s...' % sys.platform

    # find python executable: check system path, then guess
    pypath = which(pythonFile) or guessLocation(pythonFile, isOnWindows) 
    assert pypath
    pydir, pyfile = os.path.split(pypath)               # up 1 from file
    if trace:
        print 'Using this Python executable:', pypath
        raw_input('Press <enter> key')
 
    # find examples root dir: check cwd and others
    expath = guessLocation(examplesFile, isOnWindows)
    assert expath
    updir  = string.split(expath, os.sep)[:-2]          # up 2 from file
    exdir  = string.join(updir,   os.sep)               # to PP2E pkg parent
    if trace:
        print 'Using this examples root directory:', exdir
        raw_input('Press <enter> key')
 
    # export python and system paths if needed
    configSystemPath(pydir)
    configPythonPath(exdir)
    if trace:
        print 'Environment configured'
        raw_input('Press <enter> key')

    # spawn programs
    for command in commandsToStart:
        runCommandLine(pypath, os.path.dirname(expath), command, isOnWindows)


if __name__ == '__main__':
    #
    # if no args, spawn all in the list of programs below
    # else rest of cmd line args give single cmd to be spawned
    #
    if len(sys.argv) == 1:
        commandsToStart = [
            'Gui/TextEditor/textEditor.pyw',        # either slash works
            'Lang/Calculator/calculator.py',        # os normalizes path
            'PyDemos.pyw',
           #'PyGadgets.py',
            'echoEnvironment.pyw'
        ]
    else:
        commandsToStart = [ string.join(sys.argv[1:], ' ') ]
    launchBookExamples(commandsToStart)
    import time
    if sys.platform[:3] == 'win': time.sleep(10)   # to read msgs if clicked

