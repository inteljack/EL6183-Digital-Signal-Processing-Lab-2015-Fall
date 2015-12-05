###################################################################
# Use: "python fixeoln_one.py [tounix|todos] filename".
# Convert end-of-lines in the single text file whose name is passed
# in on the command line, to the target format (tounix or todos).  
# The _one, _dir, and _all converters reuse the convert function 
# here.  convertEndlines changes end-lines only if necessary:
# lines that are already in the target format are left unchanged,
# so it's okay to convert a file > once with any of the 3 fixeoln 
# scripts.  Notes: must use binary file open modes for this to 
# work on Windows, else default text mode automatically deletes 
# the \r on reads, and adds an extra \r for each \n on writes;
# Mac format not supported; PyTools\dumpfile.py shows raw bytes;
###################################################################

import os
listonly = 0   # 1=show file to be changed, don't rewrite

def convertEndlines(format, fname):                      # convert one file
    if not os.path.isfile(fname):                        # todos:  \n   => \r\n 
        print 'Not a text file', fname                   # tounix: \r\n => \n
        return                                           # skip directory names

    newlines = []
    changed  = 0 
    for line in open(fname, 'rb').readlines():           # use binary i/o modes
        if format == 'todos':                            # else \r lost on Win
            if line[-1:] == '\n' and line[-2:-1] != '\r':
                line = line[:-1] + '\r\n'
                changed = 1
        elif format == 'tounix':                         # avoids IndexError
            if line[-2:] == '\r\n':                      # slices are scaled
                line = line[:-2] + '\n'
                changed = 1
        newlines.append(line)

    if changed:
        try:                                             # might be read-only
            print 'Changing', fname
            if not listonly: open(fname, 'wb').writelines(newlines) 
        except IOError, why:
            print 'Error writing to file %s: skipped (%s)' % (fname, why)

if __name__ == '__main__':
    import sys
    errmsg = 'Required arguments missing: ["todos"|"tounix"] filename'
    assert (len(sys.argv) == 3 and sys.argv[1] in ['todos', 'tounix']), errmsg
    convertEndlines(sys.argv[1], sys.argv[2])
    print 'Converted', sys.argv[2]
