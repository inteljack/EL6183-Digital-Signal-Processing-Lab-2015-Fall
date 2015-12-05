def firstFunction(item):        
    print item                  

def count(string, chars):
    total = 0
    for x in string:
        if x in chars:
            total = total+1
    return total                # return the object 'total' refers to

x = firstFunction	
x('Hello world!')

def indirect(func, arg): func(arg)
indirect(firstFunction, 'Hello world!')

schedule = [ (firstFunction, ('Hello world!',)), (count, ([1,2,3], [2,4])) ]
for (func, args) in schedule:
    apply(func, args)
