####################################################
# this function is loaded and run by testapi.c;
# change this file between calls: auto-reload mode
# gets the new version each time 'func' is called;
# for the test, the last line was changed to:   
#     return x + y
#     return x * y
#     return x \ y     - syntax error
#     return x / 0     - zero-divide error
#     return pow(x, y)
####################################################

def func(x, y):              # called by C
    return x + y             # change me 

