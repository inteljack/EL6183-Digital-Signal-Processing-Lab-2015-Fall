>>> import glob
>>> marker = ‘::::::’
>>> for name in glob.glob(‘*.py’):      # not sys.argv
...    input = open(name, 'r')
...    print marker + name              # or to a real file...
...    print input.read(),
...

>>> import os
>>> for name in os.popen("ls *.py", ‘r’).readlines():
