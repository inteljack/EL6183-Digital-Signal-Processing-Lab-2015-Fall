This directory contains the PyErrata error reporting
system.  The root page is defined by pyerrata.html;
other files are either more html pages (.html), cgi
scripts coded in Python (.cgi), or Python support 
modules (.py) used by the cgi scripts.  Subdirectories:

- AdminTools: command-line tools for processing reports
- DbaseFiles: data storage for flat file database mode
- DbaseShelve: data storage for shelve database mode
- Mutex: a mutual exclusion file locking utility, for shelves

Note: pickle and shelve files in the Dbase* directories are
not necessarily compatible across all platforms or Python 
releases.  You may need to recreate these from scratch in
your server install.
