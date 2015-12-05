############################################################
# test custom find; the builtin find module is deprecated:
# if it ever goes away completely, replace all "import find"
# with "from PP2E.PyTools import find" (or add PP2E\PyTools
# to your path setting and just "import find"); this script 
# takes 4 seconds total time on my 650mhz Win98 notebook to
# run 10 finds over a directory tree of roughly 1500 names; 
############################################################

import sys, os, string
for dir in sys.path:
    if string.find(os.path.abspath(dir), 'PyTools') != -1:
        print 'removing', repr(dir)
        sys.path.remove(dir)   # else may import both finds from PyTools, '.'!

import find                    # get deprecated builtin (for now)
import PP2E.PyTools.find       # later use: from PP2E.PyTools import find
print  find
print  PP2E.PyTools.find

assert find.find != PP2E.PyTools.find.find        # really different?
assert string.find(str(find), 'Lib') != -1        # should be after path remove
assert string.find(str(PP2E.PyTools.find), 'PyTools') != -1 

startdir = r'C:\PP2ndEd\examples\PP2E'
for pattern in ('*.py', '*.html', '*.c', '*.cgi', '*'):
    print pattern, '=>'
    list1 = find.find(pattern, startdir)
    list2 = PP2E.PyTools.find.find(pattern, startdir)
    print len(list1), list1[-1]
    print len(list2), list2[-1]
    print list1 == list2,; list1.sort(); print list1 == list2

