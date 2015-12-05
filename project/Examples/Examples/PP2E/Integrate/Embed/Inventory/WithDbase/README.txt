This directory reuses the function-based order processing
code, but makes the inventory and buyer databases persistent
by mapping them to persistent shelves and pickled files.

The validations code and C and Python order-processing 
files were not changed to access the databases.  However, 
order lists are now loaded from a flat text file instead 
of being hard-coded in a .h or .py.  The order-processing
code was augmented with order file loading logic.

The 'Data' directory holds order list files; 'Dbase' has
the shelve and pickle files.  The Python 'validate2.py' 
validations code file is unchanged, so we just append '..'
to sys.path to import the original version from the parent
dir; we could have instead located and reused this file
by using package import paths.

