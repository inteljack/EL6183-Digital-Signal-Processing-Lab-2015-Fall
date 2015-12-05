----------------------------------------------------------------------------
This is a container directory for the entire book examples package.
The PP2E directory here is a Python module package.  Add the name of the
directory on your machine that contains PP2E (or a copy of it) to your 
PYTHONPATH setting.  See PP2E/Config/setup-pp* and PP2E/README-PP2E.txt 
for more details.  To run major Python demos from the book without such
path configuration, click the top-level PP2E/Launch_* scripts directly.
----------------------------------------------------------------------------

Details:

This directory is simply a dummy container directory for the
PP2E examples module package.  You can copy the PP2E directory
to any other directory on your machine, as long as that directory
is a package too (i.e., has a __init__.py, and is listed on the
PYTHONPATH seach-path). It's okay if the dir you copy PP2E to 
has other unrelated nested packages and modules--as long as that
container dir is on PYTHONPATH, Python will find PP2E nested there.

Because Python packages mandate that the search path must list
a directory _containing_ the one you wish to use in import 
statements, this extra parent dir level is needed.  All cross-
module imports in the book examples tree are relative to (start
at) the PP2E root directory, so you need add only the one dir
containing PP2E on your machine to PYTHONPATH.  Only imports of
modules in the same directory do not go through PP2E.

The extra PP2E nesting level makes book module imports unique
across all the Python code installed on your machine--use 
either of these import forms:

    import PP2E.xxx.yyy 
    from PP2E.xxx.yyy import name

to make sure you get book examples.  The top-level root dir 
qualifier makes these paths unique, and avoids import name clashes
in both the book examples and other modules on your machine.

Without the PP2E level, imports may load from a same-named dir or
module elsewhere, depending on on your search-path setting.  For 
instance, an import of a nested PP2E package like:

    import Gui.yyy

might mean anything on your computer, and depends completely 
on the order in your PYTHONPATH.  Without the PP2E root, 
installing another package with a "Gui" root in the path would
mean that either the book examples or the new package would be
broken (one of the two would find the wrong directory). Moreover,
installing the book examples on the path could break existing
packages the already expect a "Gui" dir--they might see things
nested in PP2E by mistake.  With the PP2E root scheme used, 
neither scenario is possible.

Note: You don't absolutely have to copy PP2E off the CD (you can
simply add PP2E's container dir on the CD to your path, or click
on the CD's PP2E\Launch_* scripts without changing your path at 
all), but copying to your hard drive allows Python to cache 
byte-code files for fast startup, and lets you change source code.

