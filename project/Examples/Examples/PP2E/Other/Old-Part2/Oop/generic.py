from types import *                     # get type constants

def action1(x, y, z): print 'action1'   # functions called by arg types
def action2(x, y, z): print 'action2'
def action3(x, y, z): print 'action3'
def action4(x, y, z): print 'action4'
def action5(x, y, z): print 'action5'

Actions =  {                            # type dispatch table
    IntType:                            # Actions[type1][type2]
        {IntType:    action1,
         StringType: action2},
    StringType:
        {ListType:   action3,           # actions can be lambda's too
         StringType: action4},
    ListType:
        {ListType:   action5}
}

def action(x, y, z):
    try:
        Actions[type(x)][type(y)](x, y, z)
    except KeyError:
        print 'bad types for action'
    

if __name__ == '__main__':
    for arg1 in (123, 'ABC', [3]):
        for arg2 in (456, 'XYZ', [4]):
            print arg1, arg2, 
            action(arg1, arg2, 'hello')
