stack = []                                # when first imported

def push(object):
    global stack                          # add item to the front
    stack = [object] + stack              # use 'global' to change

def pop():	
    global stack                          # remove item at front
    top, stack = stack[0], stack[1:]      # IndexError if empty
    return top

def empty():                              # is the stack []?
    return not stack                      # no 'global' to access
