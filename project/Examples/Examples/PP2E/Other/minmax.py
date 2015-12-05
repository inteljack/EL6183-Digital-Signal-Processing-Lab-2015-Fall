def min0(x, y):
    if x < y: 
        return x
    else:
        return y


# support multiple arguments

def min1(*args):
    res = args[0]            # start at first
    for x in args[1:]:       # scan the rest
        if x < res:
            res = x
    return res

def min2(first, *rest):
    res = first              # require one arg
    for x in rest:           # scan the rest
        if x < res:
            res = x
    return res


# generalize with functions

def extreme(compare, first, *rest):
    res = first                       # start first, scan rest
    for x in rest:                    # use passed compare func
        if compare(x, res):
            res = x
    return res

def min3(*args):
    return apply(extreme, ((lambda x, y: x < y),) + args)

def max(*args):
    return apply(extreme, ((lambda x, y: x > y),) + args)


# same, but use code strings

def extreme2(op, first, *rest):
    res = first                       # start first, scan rest
    for x in rest:                    # use passed compare optr
        if eval(str(x) + op + str(res)):
            res = x
    return res


def selftest():
    print '-'*4, min0(43, 42)
    print '-'*4, min0([[1]], [[0]])

    for func in (min1, min2, min3, max):
        print '='*4, func.__name__, '='*4
        print func(1, 2)
        print func(6, 4, 3, 1, 2)
        print func('ddd', 'ba', 'ab')
        print func([1, (2, 5)], [1, (2, 3)], [1, (2, 4)])

    print '-'*4, extreme((lambda x, y: x < y), 6, 4, 3, 1, 2)
    print '-'*4, extreme2('<', 6, 4, 3, 1, 2)
    print '-'*4, extreme2('>', 6, 4, 3, 1, 2)

if __name__ == '__main__':
    selftest()
