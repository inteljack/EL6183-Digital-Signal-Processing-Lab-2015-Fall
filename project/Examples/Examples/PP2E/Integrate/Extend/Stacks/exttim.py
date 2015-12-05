#!/usr/local/bin/python
# time the C stack module and type extensions
# versus the object chapter's Python stack implementations

from PP2E.Dstruct.Basic.timer  import test      # second count function
from PP2E.Dstruct.Basic import stack1           # python stack module 
from PP2E.Dstruct.Basic import stack2           # python stack class: +/slice
from PP2E.Dstruct.Basic import stack3           # python stack class: tuples
from PP2E.Dstruct.Basic import stack4           # python stack class: append/pop
import stackmod, stacktype                      # c extension type, module

from sys import argv
rept, pushes, pops, items = 200, 200, 200, 200  # default: 200 * (600 ops)
try:
    [rept, pushes, pops, items] = map(int, argv[1:])
except: pass
print 'reps=%d * [push=%d+pop=%d+fetch=%d]' % (rept, pushes, pops, items)

def moduleops(mod):
    for i in range(pushes): mod.push('hello')   # strings only for C
    for i in range(items):  t = mod.item(i)
    for i in range(pops):   mod.pop()

def objectops(Maker):                           # type has no init args
    x = Maker()                                 # type or class instance
    for i in range(pushes): x.push('hello')     # strings only for C
    for i in range(items):  t = x[i]
    for i in range(pops):   x.pop()

# test modules: python/c
print "Python module:", test(rept, moduleops, stack1)
print "C ext module: ", test(rept, moduleops, stackmod), '\n'

# test objects: class/type
print "Python simple Stack:", test(rept, objectops, stack2.Stack)  
print "Python tuple  Stack:", test(rept, objectops, stack3.Stack)
print "Python append Stack:", test(rept, objectops, stack4.Stack)
print "C ext type Stack:   ", test(rept, objectops, stacktype.Stack)    
