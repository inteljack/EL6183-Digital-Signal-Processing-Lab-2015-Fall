def get_option():
    for (name, func) in menu:                  # show menu items
        print '\t%s)%s' % (upper(name[0]), name[1:])
    return lower(raw_input('?'))
 
def run_option(tool):
    for (name, func) in menu:
        if tool == name[0] or tool == name:    # matches menu key?
            return func()                      # run function
    print 'what? - try again'                  # name not found
    return None                                # not really needed...

def interact():
    while 1:
        tool = get_option()
        if run_option(tool): break             # func returned 'true'?
