#!/usr/local/bin/python/python
# mail-tool, version 1
# to do: handle continued lines, etc.
# see the mail-header tools in the standard library

import sys, os
sep = '#'*80 + '\n'

if len(sys.argv) < 3:
    print 'use: ?python mtool.py <from>|* <to>|* ?<input> ?<output>'
    sys.exit(1)

From = sys.argv[1]
To   = sys.argv[2]

if len(sys.argv) > 3:
    mfile = sys.argv[3]
    if len(sys.argv) > 4:
        ofile = sys.argv[4]
    else:
        ofile = 'mtool.out'
else:
    mfile = '/usr/spool/mail/' + os.environ['USER']
    ofile = 'mtool.out'

In  = open(mfile, 'r')
Out = open(ofile, 'w')

line = In.readline()
while line:
    if line[:5] == 'From ' and (From == '*' or line[5:5+len(From)] == From):
        prefix = [sep, line]
        while line:
            line = In.readline()
            if line == '\n':
                break
            if line[:4] == 'To: ' and (To == '*' or line[4:4+len(To)] == To):
                Out.writelines(prefix)
                while line:
                    Out.write(line)
                    line = In.readline()
                    if line[:5] == 'From ': break
                break
            prefix.append(line)
    else:
        line = In.readline()

Out.close()
print 'mtool finished: see "' + ofile + '".'

