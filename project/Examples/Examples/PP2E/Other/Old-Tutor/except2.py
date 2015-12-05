try:
    just_do_it()
except IndexError:                           # exception name
    print 'Out of bounds'
except SymbolNotFound, name:                 # name, info ('raise x, y')
    print "Name '%s' not found" % name
except (e1, e2, e3):                         # if e1 or e2 or e3 raised
    pass
except:                                      # default (for all other names)
    print 'Other error'; raise FatalError
else:                                        # if no exceptions occur
    print 'No errors.'
