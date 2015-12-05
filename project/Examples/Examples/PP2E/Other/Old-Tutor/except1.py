def kaboom(list, n):
    print list[n]              # trigger IndexError

x = [0, 1, 2]
try:
    kaboom(x, 3)
except IndexError:
    print 'Hello world!'       # print 'Hello world!' the hard way... 
