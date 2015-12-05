"""
This directory is a Python modules package, that 
contains all the examples from the book Programming
Python, 2nd Edition.  There is one directory per
part of the text; each part package in turn has 
on directory for each major topic.  You can generally
import a module located anywhere in the examples 
distribution by using a full path, as long as just
this examples root directory is on PYTHONPATH.  For 
instance:

    C:\WINDOWS>set PYTHONPATH=C:\PP2ndEd\examples
    C:\WINDOWS>python
    >>> from Part2.Internet.Ftp.getfile import getfile
    >>> getfile(file='index.html',
    ...         site='starship.python.net',
    ...         dir ='public_html',
    ...         user=('lutz', 'xxxxx'))
    Downloading index.html
    Download done.
    >>>
    C:\WINDOWS>dir index.html
    INDEX~1  HTM         1,369  04-28-00 10:24a index.html

But be sure to see the README file here for more details
on lauching programs and configuring your environment.

The file you are reading identifies the examples root 
as a module package, and defines the module object that 
is created for this directory level.  The string you are 
reading becomes this module object's __doc__ attibute,
and the "from" statements below define this level's 
namespace: they simply collect all exports one level 
down, for convenience.  That's not all that convenient 
here (the __init__.py's in subdirs are empty files),
but may useful be in some apps.  I could have stuffed all 
the REDADME and *.txt files at the top of each subdirectory
into that level's __init__.py file doc strings to make them
available at the interactive command line, but I like 
separate .txt files for simplicity.

Subtle thing: a directory on PYTHONPATH makes visible the
_contents_ of that directory, not that directory itself;
to see this docstring, you need to add the parent dir:

    C:\WINDOWS>set PYTHONPATH=C:\PP2ndEd

    C:\WINDOWS>python
    >>> import examples
    >>> dir(examples)
    ['Part1', 'Part2', 'Part3', '__builtins__', '__doc__', 
    '__file__', '__name__', '__path__']
    >>> examples.__doc__
    "\012This directory is a Python modules package, that \012contains... 

    >>> import string
    >>> for line in string.split(examples.__doc__, '\n')[:4]: print line
    ...
    
    This directory is a Python modules package, that
    contains all the examples from the book Programming
    Python, 2nd Edition.  There is one directory per
    >>>
    >>> examples
    <module 'examples' from 'C:\PP2ndEd\examples\__init__.py'>
    >>> import Part2
    Traceback (innermost last):
      File "<stdin>", line 1, in ?
    ImportError: No module named Part2
    >>> import examples.Part2
"""

# real code, run when first importing at this level,
# which can only happen if parent dir is on the path;
# you should normally add examples/ to the path, not
# the parent directory of examples/, such that the code
# below isn't run if imports start at PartN's directly

# print 'Loading root'
from Part1   import *
from Part2   import *
from Part3   import *
from PyTools import *

