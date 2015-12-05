import os, sys
print 'Hello from child', os.getpid(), sys.argv[1]
raw_input("Press <Enter>")   # don't flash on Windows
