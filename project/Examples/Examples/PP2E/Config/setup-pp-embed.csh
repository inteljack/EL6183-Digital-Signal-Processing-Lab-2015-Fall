#!/bin/csh
##################################################################
# Extra settings needed for embedded Python examples only.
# To use, type 'source setup-pp-embed.csh' from a csh shell,
# or do so from your ~/.login, ~/.cshrc, etc.  This assumes
# that setup-pp.csh is sourced first, and may need to be 
# translated for other shells (e.g., bash, ksh).
#
# In most cases, Python guesses the correct source lib paths 
# from the location of the 'python' program, and always
# inspects '.', the current directory, for imported files.
# But when embedding in 1.5, and especially if you use libs
# from a custom Python build, you should add . and the python
# build tree's Lib manually.  
# 
# When embedding, Python is a liked in lib file, not the 'python'
# executable; because of this, it can have trouble automatically
# locating the standard lib dir, and may also not add '.' to the
# path on its own.  Further, if it guesses something like /usr/lib
# for standard libs, you may get version mismatch errors if you
# have a custom build.  Python may also be unable to find .so's 
# in '.' imported from Python code that is run from a C program.
# 
# You can avoid some of the following by calling special C API 
# functions to set the path, or changing Python's sys.path from 
# C, but hard-coding paths in C can be less flexible.
##################################################################

# when Python is a linked-in lib (embedding)
# prepend cwd and standard Lib in custom build tree

setenv MYPY /home/mark/python1.5.2-ddjcd/Python-1.5.2 
setenv PYTHONPATH ./$MYPY/Lib:$PYTHONPATH 

# add path to any imported external .so extension modules,
# unless imported from '.' or other dir already in path

setenv PYTHONPATH $PP2EHOME/PP2E/Integrate/Extend/Stacks:$PYTHONPATH 

