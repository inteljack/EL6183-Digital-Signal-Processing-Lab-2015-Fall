import stack2           # list-based stacks: [x]+y
import stack3           # tuple-tree stacks: (x,y)
import stack4           # in-place stacks:   y.append(x)
import timer            # general function timer function

rept = 200
from sys import argv
pushes, pops, items = eval(argv[1]), eval(argv[2]), eval(argv[3])

def stackops(stackClass):
    #print stackClass.__module__
    x = stackClass('spam')                    # make a stack object
    for i in range(pushes): x.push(i)         # exercise its methods
    for i in range(items):  t = x[i]
    for i in range(pops):   x.pop()

print 'stack2:', timer.test(rept, stackops, stack2.Stack)  # pass class to test
print 'stack3:', timer.test(rept, stackops, stack3.Stack)  # rept*(push+pop+ix)
print 'stack4:', timer.test(rept, stackops, stack4.Stack)
