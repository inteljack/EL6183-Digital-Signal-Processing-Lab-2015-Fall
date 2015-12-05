[OLD -- 1st edition's readme file; see README-PP2E.txt for new information]


This directory contains all the program examples used in
the book. For convenience, the examples directory is stored
in two formats here: 
 
- "dos/"  is for PC users
- "unix/" is for UNIX platforms
 
The "dos" version follows the MS-DOS end-of-line convention
in all text files. Other than this, the "dos" and "unix"
subdirectories are identical.
 
In some cases, you may find additional program example files
here that don't appear in the book itself. For the most part,
these are just variations on the book's examples. Filenames
here should match the code-listing labels in the book.
 
 
DIRECTORY STRUCTURE
===================
Here's how example subdirectories map to chapters in the book:
 
examples/intro              - chapter-2 examples, by section
examples/intro/shell        - [shell tools]
examples/intro/gui          - [Tkinter]
examples/intro/gui/old      - [Python1.2 versions]
examples/intro/dstruct      - [sets, stacks, etc.]
examples/intro/dbase        - [dbm, persistence]
examples/intro/text         - [strings, regex, etc.]
examples/intro/extend       - [extending, embedding]
examples/shell              - part-2, chapters 4 through 8
examples/shell/oop          - part-2, chapters 9 and 10
examples/gui                - chapter-11
examples/gui/py1.2          - chapter-11, old Python1.2 style
examples/dbase              - chapter-12
examples/dbase/test2        - chapter-12, dbm test files
examples/dstruct            - chapter-13
examples/dstruct/basic      - chapter-13, first half
examples/dstruct/classics   - chapter-13, second half
examples/extend             - chapter-14
examples/extend/modulatr    - example modulator output
examples/embed              - chapter-15
examples/lang               - chapter-16
examples/other              - appendix-A, conclusion, middle
examples/other/tutor        - appendix-E
examples/other/framewrk     - appendix-D
 
 
MANUAL CONVERSIONS
==================
If you ever find a need to convert between DOS and UNIX formats,
it's straightforword. Just copy the "examples" CD directory to
a working directory on your machine, untar with "tar -xvf" (if
needed), and run a finder script like this one:
 
---
#!/bin/csh
# pick your converter: fromdos/todos, dos2unix/unix2dos,...
 
#find ./examples -type f -print -exec fromdos {} \;
 
find ./examples -type f -print -exec dos2unix {} {} \;
---
 
There are over 400 example files in the examples directory, so
this may take a few moments on slow machines (like mine :-).
 
 
INSTALLING EXAMPLES
===================
Even if you don't need to untar or convert the examples, be sure
to copy the examples to a working directory on your machine. This
way, Python can write out ".pyc" compiled versions of the ".py"
module source files. This makes program start-ups faster (see the
book for more details).
 
For convenience, you can also add the working directory(s) to your
"PYTHONPATH" module search-path environment variable. This allows
Python to find the modules when imported, regardless of where you
are when Python is started.
 
Note: changes and updates to the program examples are probably
going to be maintained at my web-page: "http://rmi.net/~lutz".
Check there, or "http://www.ora.com" for up-to-date information.
 
 
Mark Lutz
