def genfunc(args, expr):
       exec 'def temp(%s): return %s' % (args, expr)      # def temp(args):..
       return temp                                        # sets local var

def imap(func, list):
       res = []
       for x in list: res.append(func(x))                 # run func on nodes
       return res

if __name__ == "__main__":
    def square(x): return x * x
    print imap(square, [1, 2, 3, 4])                      # [1, 4, 9, 16]
    print imap(genfunc('x', 'x * x'), [1, 2, 3, 4])       # [1, 4, 9, 16]
    print map(lambda x: x * x, [1, 2, 3, 4])              # [1, 4, 9, 16]
