#########################################################
# Use: "python fixeoln_all.py [tounix|todos] patterns?".
# find and convert end-of-lines in all text files at and
# below the directory where this script is run (the dir 
# you are in when you type 'python'). If needed, tries to 
# use the Python find.py library module, else reads the 
# output of a unix-style find command; uses a default 
# filename patterns list if patterns argument is absent.
# This script only changes files that need to be changed, 
# so it's safe to run brute-force from a root-level dir.
#########################################################

import os, sys, string
debug    = 0
pyfind   = 0      # force py find
listonly = 0      # 1=show find results only

def findFiles(patts, debug=debug, pyfind=pyfind):
    try:
        if sys.platform[:3] == 'win' or pyfind:
            print 'Using Python find'
            try:
                import find                        # use python-code find.py
            except ImportError:                    # use mine if deprecated!
                from PP2E.PyTools import find      # may get from my dir anyhow
            matches = map(find.find, patts)        # startdir default = '.'
        else:
            print 'Using find executable'
            matches = []
            for patt in patts:
                findcmd = 'find . -name "%s" -print' % patt  # run find command
                lines = os.popen(findcmd).readlines()        # remove endlines
                matches.append(map(string.strip, lines))     # lambda x: x[:-1]
    except:
        assert 0, 'Sorry - cannot find files'
    if debug: print matches
    return matches

if __name__ == '__main__':
    from fixeoln_dir import patts
    from fixeoln_one import convertEndlines

    errmsg = 'Required first argument missing: "todos" or "tounix"'
    assert (len(sys.argv) >= 2 and sys.argv[1] in ['todos', 'tounix']), errmsg

    if len(sys.argv) > 2:                  # quote in unix shell 
        patts = sys.argv[2:]               # else tries to expand
    matches = findFiles(patts)

    count = 0
    for matchlist in matches:                 # a list of lists
        for fname in matchlist:               # one per pattern
            if listonly:
                print count+1, '=>', fname 
            else:  
                convertEndlines(sys.argv[1], fname)
            count = count + 1
    print 'Visited %d files' % count
