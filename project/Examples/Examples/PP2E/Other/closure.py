def outer():
    x = 'hello'
    def inner(x=x):     # save the enclosing function's "x" 
        print x
    return inner

func = outer()
func()



def outer(x):
    return (lambda a, b=x: a + b)   # add to original "x"

func = outer('world')
func('hello')
func('bye')


func = outer('world')
func('hello', 'spam')     # overwrites saved value (default)


class counter:
    def __init__(self, start):
        self.start = start
    def close(self):
        self.start = self.start + 1
        return self.start
 
c1 = counter(10).close          # bound-method objects retain 'self'
c2 = counter(24).close          # 'self' retains the original values
print c1(), c2(), c1(), c2()


class counter:
    def __init__(self, start):
        self.start = start
    def __call__(self):
        self.start = self.start+1
        return self.start

c1 = counter(10)                # callable class-instance objects
c2 = counter(24)                # 'self' retains original values
print c1(), c2(), c1(), c2()
