# rename files with all lower case
# some dos tools make them all upper
# cmdline arg is name pattern (ex: *.*)
# see also: fixnames_all.py

import os, sys, string
from glob import glob

for name in glob(sys.argv[1]):
    print name
    os.rename(name, string.lower(name))
