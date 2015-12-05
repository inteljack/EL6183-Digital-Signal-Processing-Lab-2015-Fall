################################################################################
# extra entry-points for App class tree
################################################################################

import sys, os, string
from PP2E.System.App.Bases.app      import *  # use this file to get everything
from PP2E.System.App.Kinds.internal import *  # or import from specific module
from PP2E.System.App.Kinds.interact import *
from PP2E.System.App.Kinds.redirect import *


################################################################################
# Mix-in class examples: __init__ taken from RedirectInternalApp.
# The result (stdout output string) is returned from App.main() call.
#
# Multiple-inheritance name resolution is depth-first, l-top-r.
# We need InteractiveApp's run(), and RedirectInternalApp's __init__(),
# so there's a problem with either:
#
# class TestInteractiveApp(RedirectInternalApp, InteractiveApp): 
#     pass      # wrong run!
#
# class TestInteractiveApp(InteractiveApp, RedirectInternalApp): 
#     pass      # wrong __init__!
#
# Two solutions are illustrated in the 2 mix-in classes here.
# Note: this subclassing technique can be used to test any class 
# derived from App (pack, mtool..): inherit from the tested class 
# plus RedirectInternalApp, and resolve conflicts manually (or use 
# FuncTestApp below, on the top-level entry-point in the tree).
# The "run =" is like "def run(self): InteractiveApp.run(self)" 
################################################################################


class TestInteractiveApp(RedirectInternalApp, InteractiveApp): 
    run = InteractiveApp.run

class TestMenuApp(MenuDictApp, RedirectInternalApp): 
    __init__ = RedirectInternalApp.__init__ 
    stop     = RedirectInternalApp.stop              # resolve conflicts
    closeApp = RedirectInternalApp.closeApp          # by manual assignment


################################################################################
# Top-level external entry points (non-oop)
# 
# import app
# from mtool2 import MtoolApp
# app.appCall(MtoolApp, '-x', '-i', '/home/lutz/mbox', '-t', 'steve')
#
# import app
# app.appRun('mtool2.py', '-i', '/home/lutz/mbox', '-f', 'andy', '-o', '-')
# app.appRun('mtool2.py', '-i /home/lutz/mbox', '-f andy -o -')
#
# _buildArgs() flattens the arguments passed in, splits multi-arg
# strings, and converts non-strings to strings.  List/tuple trees
# can be constructed and passed in-- flattened into a list of strings,
# and/or args can be passed in as args to appCall (varargs);
################################################################################

def _buildArgs(args):
    res = []
    for arg in args:
        if type(arg) in [type([]), type(())]:
            res = res + _buildArgs(arg)         # ['a', '-b', (1, 2)]
        elif type(arg) != type(''):
            res.append(`arg`)                   # 1 2.2 
        else:
            res = res + string.split(arg)       # "f1 f2 f3"
    return res

def appCall(appClass, *args):                   # call an App like a function
    save_argv = sys.argv
    sys.argv  = [appClass.__name__] + _buildArgs(args)
    result    = appClass().main()
    sys.argv  = save_argv
    return result

def appRun(script, *args):                      # run as a new process 
    arglist = _buildArgs(args)                  # or: ScriptOutput(s,a).read()
    cmdline = script + ' ' + string.join(arglist)
    return os.popen(cmdline, 'r').read()


################################################################################
# Treat an App run like a file.
# Here, read/write mean the view outside an app, instead of the app itself 
# (not it's i/o streams).  ScriptPipe.write() sends data to the app, and
# ScriptPipe.read() gets the app's output. 
################################################################################

class ScriptPipe:
    def __init__(self, cmdline, mode):    
        self.pipe = os.popen(cmdline, mode)   # closed on deletion

    def __getattr__(self, name):
        return getattr(self.pipe, name)       # delegate to pipe file

    def cmdline(self, script, args):
        return script + ' ' + string.join(_buildArgs(args))

class ScriptOutput(ScriptPipe):               # use .read, .readline(),...
    def __init__(self, script, *args):
        ScriptPipe.__init__(self.cmdline(script, args) + " -o -", 'r')

class ScriptInput(ScriptPipe):                # use .write(), .writelines(),...
    def __init__(self, script, *args):
        ScriptPipe.__init__(self.cmdline(script, args) + " -i -", 'w')


################################################################################
# Simple i/o redirection
# Note: we can't rely on App.__del__ to restore streams when App.main()
# returns: __del__ won't run if any ref's to the App instance remain.
# (Example: if any get*() call fails, there's a traceback object with
# a reference).  Without App.closeApp, we'd have to call __del__ here.
################################################################################

def _redirected1(input, function, args):             # the hard way...
    save_streams = sys.stdin, sys.stdout
    sys.stdin    = Input(input)
    sys.stdout   = Output()
    try:
        apply(function, args)
    except:
        sys.stderr.write('error in function! ')
        sys.stderr.write(`sys.exc_type` + ',' + `sys.exc_value` + '\n')
    result = sys.stdout.text
    sys.stdin, sys.stdout = save_streams
    return result


class FuncTestApp(RedirectInternalApp):              # the way of tao...
    def __init__(self, input, func, args):
        RedirectInternalApp.__init__(self, input)
        self.call = func, args
    def run(self):
        #try:
            apply(apply, self.call)
        #except: 
        #    self.message('error in function!' + `self.exception()`)

def redirected(input, function, args):
    return FuncTestApp(input, function, args).main()

