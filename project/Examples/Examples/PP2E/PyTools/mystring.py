"""
================================================================================
Map string module functions to string object methods (possible future patch).

Synopsis:
Use this as a patch if and only if the standard string module is ever 
deleted from the standard Python library in a future incompatible Python 
release.  This module is completely unnecessary for the current Python 
releases (1.5 and 2.0--the versions included on the book CD), and might 
never be required in the future.  See the string module sections near
the start of chapters 2 and 18 of the book for background details.

Details:
Just before the final draft of this book was submitted, Python creator 
Guido van Rossum posted a note that seemed to imply that the standard 
"string" module might go way in a future release, tentatively called 
"Python 3000".  This release, if it ever does materialize, is likely years
down the road, but will be a full break with the past, and will introduce 
arbitrary non-backward-compatible changes to the Python language.

The string module has been used in virtually every Python program ever 
written in the last decade, and is one of the primary tools employed by 
the half-million Python users in the world today, so it's not at all clear
that it will go away even in a "Python 3000".  However, if this release 
abandons the notion of backward compatibility in general, the loss of the 
string module may be just one of large set of code breakages.

If (and only if) the string module is no longer part of the Python standard
library in the future, and you've gotten this second edition after that 
change but before a book update, you can work around the issue by changing
example source-code to import this module instead of the standard string 
module.  That is, change all:
    "import string" and 
    "from string import X"
to:
    "from PP2E.PyTools import mystring as string" and 
    "from PP2E.PyTools.mystring import X"

The latter forms load this module, which simply serves to map traditional 
string module function calls to new string object method calls. For 
instance:
    "string.split(x)" maps to "x.split()"
  
Note that some of the wrapper functions below may not be 100% complete or 
compatible with the original module; change as needed.  You can also simply
change the examples to use string methods directly (and this solution will 
run faster).  In principle, you might even write a Python script that 
performs such changes automatically (e.g., with the tree walker tools in 
the first part of the book, and the parsing techniques in the fourth).  
At the least, the import statement changes above could be so automated.  
Watch this book's we site at http://rmi.net/~lutz/about-pp2e.html for 
updated example downloads, and/or automated program conversion tools for
future Python releases.  Other future changes are not addressed by this file.

This is a hack which will hopefully never be needed, and I wish I had
a better story to tell on this front.  Python releases have thus far 
strived to maintain a very high degree of backward compatibility.  But
there is no real Python language standard today, and the rate of Python
change is accelerating.  Regrettably, such changes seem more and more to be 
beyond the control of both book authors and the masses of common developers
doing real work with Python.  If such change concerns you or your company, 
please direct your concerns to python-dev@python.org, the Python language 
developers email list.  It's your Python, after all.
================================================================================
"""

def split(str, *args):        return apply(str.split, args)
def join(str, *args):         return apply(str.join, args)
def replace(str, *args):      return apply(str.replace, args)

def atof(str, *args):         return apply(str.atof, args)
def atoi(str, *args):         return apply(str.atoi, args)
def atol(str, *args):         return apply(str.atol, args)

def capitalize(str, *args):   return apply(str.capitalize, args)
def expandtabs(str, *args):   return apply(str.expandtabs, args)
def swapcase(str, *args):     return apply(str.swapcase, args)

def find(str, *args):         return apply(str.find, args)
def rfind(str, *args):        return apply(str.rfind, args)
def index(str, *args):        return apply(str.index, args)
def rindex(str, *args):       return apply(str.rindex, args)
def count(str, *args):        return apply(str.count, args)

def lower(str, *args):        return apply(str.lower, args)
def upper(str, *args):        return apply(str.upper, args)

def strip(str, *args):        return apply(str.strip, args)
def lstrip(str, *args):       return apply(str.lstrip, args)
def rstrip(str, *args):       return apply(str.rstrip, args)

def ljust(str, *args):        return apply(str.ljust, args)
def rjust(str, *args):        return apply(str.rjust, args)
def center(str, *args):       return apply(str.center, args)
def zfill(str, *args):        return apply(str.zfill, args)


# not that a class __getattr__ won't help here, because this
# is a simple module imported as a whole, and __getattr__ sends
# just the attribut name, not the subject string object.


try:
    from stringconstants import *      # non-functions here?
except ImportError:                    # else add in this file
    pass

if __name__ == '__main__':             # self-test (pre-2.0)
    import string
    class dummy:
        def __getattr__(self, name):
            print 'calling str.%s' % name,
            return self.callit
        def callit(self, *args):
            print '\twith', args

    str = dummy()
    split(str, '+++')
    replace(str, 'spam', 'SPAM')
    find(str, 'gumby')
    str.find('brian')

################################################
# C:\...\PP2E\PyTools>python mystring.py
# calling str.split       with ('+++',)
# calling str.replace     with ('spam', 'SPAM')
# calling str.find        with ('gumby',)
# calling str.find        with ('brian',)
################################################