# feedbackdelay_circbuffer2_test01.py
# Impulse response of a delay with feedback.
# y(n) = x(n-N) + Gfb y(n-N)
# This implementation uses a circular buffer with
# two buffer indices.

# Set parameters of delay system
Gfb = 0.5       # feed-back gain
N = 5           # Delay (in samples)

# Create a delay line (buffer) to store past values. Initialize to zero.
buffer_length = 10      # buffer_length > N
buffer = [ 0.0 for i in range(buffer_length) ]    

# Delay line (buffer) index
kr = 0      # read 
kw = N      # write

for i in range(31):
    
    print('y({0:2d}) = {1:f}'.format(i, buffer[kr]))

    # Use impulse as input signal
    if i == 0:
        input_value = 1
    else:
        input_value = 0

    # Update buffer
    buffer[kw] = input_value + Gfb * buffer[kr]

    # Increment buffer indices    
    kr += 1
    if kr == buffer_length:
        # We have reached the end of the buffer. Circle back to front.
        kr = 0

    kw += 1
    if kw == buffer_length:
        # We have reached the end of the buffer. Circle back to front.
        kw = 0

