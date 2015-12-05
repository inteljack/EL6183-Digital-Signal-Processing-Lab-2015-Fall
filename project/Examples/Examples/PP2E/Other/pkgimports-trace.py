#######################################################################
# 1.5 Package import variations -- additional trace info
# Each subpath of the full package path is added to sys.modules as 
# soon as the first import happens; 'from' adds more specific names 
# to the importing namespace; 'import' adds the leftmost directory's 
# name (nested parts to the right are available as attributes);
# output:
# 
# [mark@toy ~/PP2ndEd/dev/examples]$ python pkgimports-trace.py
# <function test at 80ccba0>
# 
# dir() = ['__doc__', 'test', '__name__', 'dumpdir', '__builtins__', 'dumpsys', 'sys']
# 
# sys.modules = ['os.path', 'os', 'Part2.Dstruct.Basic.timer', 'exceptions', '__main__', 'posix', 'Part2', 'sys', '__builtin__', 'site', 'Part2.Dstruct.Basic', 'Part2.Dstruct', 'signal', 'UserDict', 'posixpath', 'stat']
# 
# <function test at 80ccba0>
# <module 'Part2' from 'Part2/__init__.pyc'>
# 
# dir() = ['__doc__', 'test', '__name__', 'dumpdir', '__builtins__', 'dumpsys', 'Part2', 'sys']
# 
# sys.modules = ['os.path', 'os', 'Part2.Dstruct.Basic.timer', 'exceptions', '__main__', 'posix', 'Part2', 'sys', '__builtin__', 'site', 'Part2.Dstruct.Basic', 'Part2.Dstruct', 'signal', 'UserDict', 'posixpath', 'stat']
# 
# <function test at 80ccba0>
# 
# dir() = ['timer', '__doc__', 'test', '__name__', 'dumpdir', '__builtins__', 'dumpsys', 'Part2', 'sys']
# 
# sys.modules = ['os.path', 'os', 'Part2.Dstruct.Basic.timer', 'exceptions', '__main__', 'posix', 'Part2', 'sys', '__builtin__', 'site', 'Part2.Dstruct.Basic', 'Part2.Dstruct', 'signal', 'UserDict', 'posixpath', 'stat']
# 
#######################################################################

import sys

def dumpdir():
    print '\ndir() = %s\n' % globals().keys()        # like dir outside func

def dumpsys():
    print 'sys.modules = %s\n' % sys.modules.keys()  # loaded module names


from Part2.Dstruct.Basic.timer import test      # name 'test' assigned
print test                                      # all path names in sys.modules

dumpdir()
dumpsys()

import Part2.Dstruct.Basic.timer                # name 'Part2' assigned
print  Part2.Dstruct.Basic.timer.test 
print Part2

dumpdir()
dumpsys()

from Part2.Dstruct.Basic import timer           # name 'timer' assigned
print timer.test

dumpdir()
dumpsys()

