#######################################################################
# 1.5 Package import variations
# Modules packages add syntax to 'import' and 'from' statements 
# that lets you specify a directory path where to a module
# resides on your machine: the module name can take the form
# 'dir.dir.dir.name'.  Essentially, you can either say:
# 
# 1) "from dir1.dir2.dir3 import x"
#       and use the name "x" in the importer (not "dir1")
#
# 2) "import dir1.dir2.dir3.x"
#       and use the name "dir1" in the importer (not "x")
#       or use "dir1.dir2", "dir1.dir2.dir3", "dir1.dir2.dir3.x"
# 
# In both cases "dir1" must be found within a directory listed on 
# the Python module search-path (sys.path, usually initialized from
# youe PYTHONPATH shell variable setting), and all dirs along a 
# module'svdirectory path must have an __init__.py file used as that
# level's module names (and used to identify the name as a package).
#
# The "from" form above (1) is generally more maintainable, because
# you need code the directory path in your script only once--at the
# "from" statement (the import form implies coding the full dir
# path everywhere you access the end name: "dir.dir...dir.x").
#
# __init__.py can also have a doc string at the top (to doc a
# whole directory), use multiple "from submod import *" to collect
# all names in all contained modules, run glob commands, and so on.
#
# C:\Stuff\Mark\Writing\PP2ndEd\dev\examples>python
# >>> from Part2.Dstruct.Basic import timer
# >>> timer
# <module 'Part2.Dstruct.Basic.timer' from 'Part2\Dstruct\Basic\timer.pyc'>
# >>> Part2
# Traceback (innermost last):
#   File "<stdin>", line 1, in ?
# NameError: Part2
# >>> dir()
# ['__builtins__', '__doc__', '__name__', 'timer']
# 
# C:\Stuff\Mark\Writing\PP2ndEd\dev\examples>python
# >>> import Part2.Dstruct.Basic.timer
# >>> Part2
# <module 'Part2' from 'Part2\__init__.pyc'>
# >>> timer
# Traceback (innermost last):
#   File "<stdin>", line 1, in ?
# NameError: timer
# >>> Part2.Dstruct.Basic.timer
# <module 'Part2.Dstruct.Basic.timer' from 'Part2\Dstruct\Basic\timer.pyc'>
# >>> Part2.Dstruct
# <module 'Part2.Dstruct' from 'Part2\Dstruct\__init__.pyc'>
# >>> dir()
# ['Part2', '__builtins__', '__doc__', '__name__']
#
# About this script:
# Access function "test" in file "$PP2E/Part2/Dstruct/Basic/timer.py", 
# assuming we're at $PP2E, or $PP2E is on PYTHONPATH ($PP2E is where
# you've copied the examples root, /home/mark/PP2ndEd/dev/examples 
# on my machine).  For package imports, the leftmost component must 
# be on the path, and the rest must all be subdirectories that
# contain __init__.py files.  You could also simply put the full 
# directory leading to timer.py on PYTHONPATH and avoid the 
# dotted packed import forms here; but packages are nice when
# there may be more than one file with the same name--PYTHONPATH
# only supports finding one, unless sys.path is changed dynamically. 
# PYTHONPATH gives start point; import/from statements give extensions
# below dirs on PYTHONPATH; note: if have a dir "xxx" with an __init__.py
# and a file "xxx.py" at same level, Python imports dir "xxx" using defs
# in its __init__.py to represent module namespace; can also have a 
# "xxx.so" in same dir--use diff names or dirs!
# Output:
# 
# [mark@toy ~/PP2ndEd/dev/examples]$ python pkgimports.py
# <function test at 80f39c8>
# <function test at 80f39c8>
# <function test at 80f39c8>
# <function test at 80f39c8>
# <module 'Part2' from 'Part2/__init__.pyc'>
# <module 'Part2.Dstruct' from 'Part2/Dstruct/__init__.pyc'>
# <module 'Part2.Dstruct.Basic' from 'Part2/Dstruct/Basic/__init__.pyc'>
# <module 'Part2.Dstruct.Basic.timer' from 'Part2/Dstruct/Basic/timer.pyc'>
# <function test at 80f39c8>
# <module 'Part2.Dstruct.Basic.timer' from 'Part2/Dstruct/Basic/timer.pyc'>
#
# Also see how the timer module is used in Part3/Extend/Stacks, and 
# package-based reloading notes in Part3/Embed/TestApi/WithPackages.
#
# C:\Stuff\Mark\Writing\PP2ndEd\dev\examples>python
# Python 1.5.2 (#0, Apr 13 1999, 10:51:12) [MSC 32 bit (Intel)] on win32
# Copyright 1991-1995 Stichting Mathematisch Centrum, Amsterdam
# >>> import Part2.Dstruct.Basic.timer
# >>> dir()
# ['Part2', '__builtins__', '__doc__', '__name__']
# >>> timer.test()
# Traceback (innermost last):
#   File "<stdin>", line 1, in ?
# NameError: timer
# >>> Part2
# <module 'Part2' from 'Part2\__init__.pyc'>
# >>> import sys
# >>> for k in sys.modules.keys():
# ...    if k[:5] == 'Part2': print sys.modules[k]
# ...
# <module 'Part2.Dstruct.Basic.timer' from 'Part2\Dstruct\Basic\timer.py'>
# <module 'Part2' from 'Part2\__init__.pyc'>
# <module 'Part2.Dstruct.Basic' from 'Part2\Dstruct\Basic\__init__.py'>
# <module 'Part2.Dstruct' from 'Part2\Dstruct\__init__.pyc'>
# >>>
# >>> Part2.Dstruct.Basic.timer.test
# <function test at 798a20>
# >>> timer
# Traceback (innermost last):
#   File "<stdin>", line 1, in ?
# NameError: timer
# >>> Basic
# Traceback (innermost last):
#   File "<stdin>", line 1, in ?
# NameError: Basic
#
# C:\Stuff\Mark\Writing\PP2ndEd\dev\examples>python
# Python 1.5.2 (#0, Apr 13 1999, 10:51:12) [MSC 32 bit (Intel)] on win32
# Copyright 1991-1995 Stichting Mathematisch Centrum, Amsterdam
# >>> from Part2.Dstruct.Basic import timer
# >>> Part2
# Traceback (innermost last):
#   File "<stdin>", line 1, in ?
# NameError: Part2
# >>> timer
# <module 'Part2.Dstruct.Basic.timer' from 'Part2\Dstruct\Basic\timer.pyc'>
# >>> timer.test
# <function test at 796ec0>
# >>> Basic
# Traceback (innermost last):
#   File "<stdin>", line 1, in ?
# NameError: Basic
# >>> import sys
# >>> for k in sys.modules.keys():
# ...     if k[:5] == 'Part2': print sys.modules[k]
# ...
# <module 'Part2.Dstruct.Basic.timer' from 'Part2\Dstruct\Basic\timer.pyc'>
# <module 'Part2' from 'Part2\__init__.pyc'>
# <module 'Part2.Dstruct.Basic' from 'Part2\Dstruct\Basic\__init__.pyc'>
# <module 'Part2.Dstruct' from 'Part2\Dstruct\__init__.pyc'>
#
#######################################################################


# basic use

from Part2.Dstruct.Basic.timer import test     # name 'test' assigned
print test                                     # paths put on sys.modules

import Part2.Dstruct.Basic.timer               # name 'Part2' assigned
print  Part2.Dstruct.Basic.timer.test 

from Part2.Dstruct.Basic import timer          # name 'timer' assigned
print timer.test


# can assign paths to shorter names

mod = Part2.Dstruct.Basic.timer 
print mod.test


# this fails - name timer isn't available by itself
# print timer.test


# each component can be imported by itself

import Part2
print  Part2

import Part2.Dstruct
print  Part2.Dstruct

from Part2.Dstruct import Basic
print Basic


# this fails - names in import/from refer to external files, not objects
# from Basic import timer
# print timer

print Basic.timer
print Basic.timer.test

import Part2.Dstruct.Basic
print  Part2.Dstruct.Basic.timer
