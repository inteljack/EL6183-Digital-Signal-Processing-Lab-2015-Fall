def test(reps, func):                                                           
    import time
    start_wall = time.time()                  # current real seconds
    start_cpu  = time.clock()                 # current processor secs   
    for i in xrange(reps):                    # call it 'reps' times
        x = func(i) 
    cpu_time  = time.clock() - start_cpu    
    wall_time = time.time()  - start_wall     # total = stop - start time 
    return {'cpu': cpu_time, 'wall': wall_time}
