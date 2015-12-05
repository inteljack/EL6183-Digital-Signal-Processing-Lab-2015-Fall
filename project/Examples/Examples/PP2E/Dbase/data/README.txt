Note that all the example shelve/dbm data files
have a "-152" appended to their names as given in
the book.

Even with the name extensions, these files are 
only guaranteed to be compatible with the Windows 
version of Python 1.5.2--such files can only be 
read by the DBM file system used to create them,
and are not necessarily portable across platforms
or Python releases.  On other platforms or Python
releases, you should recreate the data files anew,
as demonstrated in the text. 

