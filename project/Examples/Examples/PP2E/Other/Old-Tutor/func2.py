def optional(real, *rest):
    for arg in rest: print arg,      # rest is a tuple of arguments

def default(real, a=1, b=2):
    print a, b
