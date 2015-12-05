#!/usr/bin/python
import glob, pickle
 
def dump(kind):
    print '\n', kind, '='*60, '\n'
    for file in glob.glob("../DbaseFiles/%s/*.data" % kind):
        print '\n', '-'*60
        print file
        print pickle.load(open(file, 'r'))

dump('errataDB')
dump('commentDB')

