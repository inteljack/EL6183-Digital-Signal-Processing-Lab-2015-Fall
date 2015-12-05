#########################################################################
# Use: "python fixeoln_one.py [tounix|todos|tomac] filename".
# Adds supprt for converting to and from Macintosh \r terminators.
# !BUG! Conversions _to_ Mac form work, but conversions _from_ files
# aready on Mac format to Unix or Dos fail when this runs on Windows, 
# because the file.readline function treats the entire file as one 
# long line. If this is not a readline bug, then you'd have to use 
# file.read and look for end-lines manually or fall back on something
# like: string.join(string.split(line, '\r'), '\n') for each line.
# This may work okay on the Mac port (else readline won't either!)
#########################################################################

import os
listonly = 0

def convertEndlines(format, fname):                     # convert one file
    if not os.path.isfile(fname):                       # skip directory names 
        print 'Not a text file', fname                  # use binary file i/o
        return                                          # to avoid auto-mapping

    newlines = []
    changed  = 0
    for line in open(fname, 'rb').readlines():
        if format == 'todos':                           # [x\n, \r] => \r\n
            if (line[-1:] == '\r' or 
               (line[-1:] == '\n' and line[-2:-1] != '\r')):
                line = line[:-1] + '\r\n'
                changed = 1
        elif format == 'tounix':                        # [\r, \r\n] => \n
            if line[-1:] == '\r': 
                line = line[:-1] + '\n'
                changed = 1
            elif line[-2:] == '\r\n': 
                line = line[:-2] + '\n'
                changed = 1
        elif format == 'tomac':                         # [\n, \r\n] => \r
            if line[-1:] == '\n':
                line = line[:-1]
                if line[-1:] != '\r':
                    line = line + '\r'
                changed = 1
        newlines.append(line)

    if changed:                                          # might be read-only
        try:
            print 'Changing', fname
            if not listonly: open(fname, 'wb').writelines(newlines)
        except IOError, why:
            print 'Error writing to file %s: skipped (%s)' % (fname, why)

if __name__ == '__main__':
    import sys
    errmsg = 'Required arguments missing: [ todos | tounix | tomac ] <filename>'
    assert (len(sys.argv) == 3 and
            sys.argv[1] in ['todos', 'tounix', 'tomac']), errmsg
    convertEndlines(sys.argv[1], sys.argv[2])
    print 'Converted', sys.argv[2]
