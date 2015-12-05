stack = []

def push(data):
    global stack                          # changes a global
    stack = [data] + stack                # add node to front

def pop():	
    global stack
    top, stack = stack[0], stack[1:]      # delete front node
    return top

def empty(): return not stack	       
