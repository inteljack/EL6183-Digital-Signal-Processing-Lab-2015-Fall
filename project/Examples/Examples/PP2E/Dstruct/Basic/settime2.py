from settime import doit
import set, fastset

import timer, sys
print 'start...'
print timer.test(eval(sys.argv[1]), lambda i: doit(set.Set, i))
print timer.test(eval(sys.argv[1]), lambda i: doit(fastset.Set, i))
