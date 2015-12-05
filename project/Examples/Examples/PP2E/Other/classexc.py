####################################
# class exceptions, funcs to raise
# Sub matches Super in an except
####################################

class Super: 
    def __init__(self, value):
        self.errno = value

class Sub(Super): 
    def extra(self):
        return self.errno * 2

def raiser1():
    raise Super(8)

def raiser2():
    raise Sub(9)

####################################
# catch Super and all its subclasses
# get raised class/instance from sys
####################################

print 
for func in (raiser1, raiser2):
    try:
        func()
    except Super:
        import sys
        print 'caught', sys.exc_type, sys.exc_value

####################################
# catch Super and all its subclasses
# get raised instance as extra data
####################################

print 
for func in (raiser1, raiser2):
    try:
        func()
    except Super, instance:
        print 'caught', instance.__class__, instance.errno
        if instance.__class__ == Sub:
            print 'extra call', instance.extra()

