def test(reps, func, *args):                                                           
    import time
    start = time.clock()            # current CPU tim in float seconds
    for i in xrange(reps):          # call function reps times
        apply(func, args)           # discard any return value                             
    return time.clock() - start     # stop time - start time                                     
