#################################################################
# run PyEdit without DOS console popup for os.system on Windows;
# at present, ".pyw" files cannot be imported as modules;
# if you want a file to be both a program that launches without
# a dos console box on windows, and be imported from elsewhere,
# use ".py" for the main file and import .py code from a ".pyw";
# execfile('textEditor.py') fails when run from another dir,
# because the current working dir is the dir I'm run from;
#################################################################

import textEditor             # grab .py (or .pyc) file
textEditor.main()             # run top-level entry point

