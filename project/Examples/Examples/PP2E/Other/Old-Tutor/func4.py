def countDown(N):
    if N == 0:                    # stop the call chain
        print 'Hello world!'
    else:
        print N; countDown(N-1)   # call myself again: N, N-1, N-2,...0
