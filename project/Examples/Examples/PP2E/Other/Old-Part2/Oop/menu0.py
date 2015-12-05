from string import upper, lower

def interact_dict(menu):                           # pass in menu (not global)
    while 1:
        for name in menu.keys(): 
            print '\t' + name                      # show options
        tool = raw_input('?')
        try:
            menu[tool]()                           # run function
        except KeyError:              
            print 'what? - try again'              # key not found

def interact_list(menu):                           # pass in menu here too
    while 1:
        for name, func in menu:                
            print '\t' + upper(name[0]) + ')' + name[1:]  
        tool = lower(raw_input('?'))
        for name, func in menu:
            if tool == name[0] or tool == name:    # matches menu key?
                exitflag = func()                  # run function
                break                           
        else:
            print 'what? - try again'              # not found: goto while
            continue                         
        if exitflag: break                         # exit while if 'true'

def interact(menu):
    try:
        if type(menu) == type([]):             # do type-testing
            interact_list(menu)
        elif type(menu) == type({}):           # 'switch' on the menu's type
            interact_dict(menu)
        else:
            print "bad menu: must be a list or dictionary"
    except EOFError: pass
