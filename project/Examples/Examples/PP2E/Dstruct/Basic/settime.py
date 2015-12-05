import timer, sys
import set, fastset

def setops(Class):
    a = Class(range(50))                 # a 50-integer set
    b = Class(range(20))                 # a 20-integer set
    c = Class(range(10))
    d = Class(range(5))
    for i in range(5):
        t = a & b & c & d                # 3 intersections
        t = a | b | c | d                # 3 unions

if __name__ == '__main__':
    rept = int(sys.argv[1]) 
    print 'set =>    ', timer.test(rept, setops, set.Set)
    print 'fastset =>', timer.test(rept, setops, fastset.Set)
