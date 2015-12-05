import os                                  # delete old output files in tree
from PP2E.PyTools.find import find         # only need full path if I'm moved
for filename in find('*.out.txt'):         # use cat instead of type in Linux
    print filename
    if raw_input('View?') == 'y':
        os.system('type ' + filename)
    if raw_input('Delete?') == 'y':
        os.remove(filename)

