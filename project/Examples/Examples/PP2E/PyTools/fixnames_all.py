#########################################################
# Use: "python ..\..\PyTools\fixnames_all.py".
# find all files with all upper-case names at and below
# the current directory ('.'); for each, ask the user for
# a new name to rename the file to; used to catch old 
# uppercase file names created on MS-DOS (case matters on
# some platforms, when importing Python module files);
# caveats: this may fail on case-sensitive machines if 
# directory names are converted before their contents--the
# original dir name in the paths returned by find may no 
# longer exist; the allUpper heuristic also fails for 
# odd filenames that are all non-alphabetic (ex: '.');
#########################################################

import os, string
listonly = 0

def allUpper(name):
    for char in name:
        if char in string.lowercase:    # any lowercase letter disqualifies
            return 0                    # else all upper, digit, or special 
    return 1 

def convertOne(fname):
    fpath, oldfname = os.path.split(fname)
    if allUpper(oldfname):
        prompt = 'Convert dir=%s file=%s? (y|Y)' % (fpath, oldfname)
        if raw_input(prompt) in ['Y', 'y']:
            default  = string.lower(oldfname)
            newfname = raw_input('Type new file name (enter=%s): ' % default)
            newfname = newfname or default
            newfpath = os.path.join(fpath, newfname)
            os.rename(fname, newfpath)
            print 'Renamed: ', fname
            print 'to:      ', str(newfpath)
            raw_input('Press enter to continue')
            return 1
    return 0

if __name__ == '__main__':
    patts = "*"                              # inspect all file names
    from fixeoln_all import findFiles        # reuse finder function
    matches = findFiles(patts)

    ccount = vcount = 0
    for matchlist in matches:                # list of lists, one per pattern
        for fname in matchlist:              # fnames are full directory paths
            print vcount+1, '=>', fname      # includes names of directories 
            if not listonly:  
                ccount = ccount + convertOne(fname)
            vcount = vcount + 1
    print 'Converted %d files, visited %d' % (ccount, vcount)
