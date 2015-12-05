#########################################################
# Usage: "python diffall.py dir1 dir2".
# recursive tree comparison--report files that exist 
# in only dir1 or dir2, report files of same name in 
# dir1 and dir2 with differing contents, and do the 
# same for all subdirectories of the same names in 
# and below dir1 and dir2; summary of diffs appears 
# at end of output (but search redirected output for 
# "DIFF" and "unique" strings for further details);
#########################################################

import os, dirdiff

def intersect(seq1, seq2):
    commons = []               # items in seq1 and seq2
    for item in seq1:
        if item in seq2:
            commons.append(item)
    return commons

def comparedirs(dir1, dir2, diffs, verbose=0):
    # compare filename lists
    print '-'*20
    if not dirdiff.comparedirs(dir1, dir2):
        diffs.append('unique files at %s - %s' % (dir1, dir2))

    print 'Comparing contents'
    files1 = os.listdir(dir1)
    files2 = os.listdir(dir2)
    common = intersect(files1, files2)

    # compare contents of files in common
    for file in common:
        path1 = os.path.join(dir1, file)
        path2 = os.path.join(dir2, file)
        if os.path.isfile(path1) and os.path.isfile(path2):
            bytes1 = open(path1, 'rb').read()
            bytes2 = open(path2, 'rb').read()
            if bytes1 == bytes2:
                if verbose: print file, 'matches'
            else:
                diffs.append('files differ at %s - %s' % (path1, path2))
                print file, 'DIFFERS'

    # recur to compare directories in common
    for file in common:
        path1 = os.path.join(dir1, file)
        path2 = os.path.join(dir2, file)
        if os.path.isdir(path1) and os.path.isdir(path2):
            comparedirs(path1, path2, diffs, verbose)

if __name__ == '__main__':
    dir1, dir2 = dirdiff.getargs()
    mydiffs = []
    comparedirs(dir1, dir2, mydiffs)        # changes mydiffs in-place
    print '='*40                            # walk, report diffs list
    if not mydiffs:
        print 'No diffs found.'
    else:
        print 'Diffs found:', len(mydiffs)
        for diff in mydiffs: print '-', diff

