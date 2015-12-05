def interact(menu):
    try:
        if type(menu) == type({}):               # dictionaries first
            while 1:
                for name in menu.keys(): 
                    print '\t' + name            # show options
                tool = raw_input('?')
                try:
                    menu[tool]()                 # run function
                except KeyError:                 # sys.exit to end
                    print 'what? - try again'

        elif type(menu) == type([]):             # lists added later...
            from string import upper, lower
            while 1:
                for name, func in menu:                
                    print '\t' + upper(name[0]) + ')' + name[1:]  
                tool = lower(raw_input('?'))
                for name, func in menu:
                    if tool == name[0] or tool == name:  
                        exitflag = func()            
                        break                    # run function
                else:
                    print 'what? - try again'    # not found: goto while
                    continue                         
                if exitflag: break               # exit while if 'true'

        elif type(menu) == type(''):
            pass  # handle string-based menus in the future...

        else:
            print "bad menu type: not a list, dictionary, or string"

    except EOFError: pass
