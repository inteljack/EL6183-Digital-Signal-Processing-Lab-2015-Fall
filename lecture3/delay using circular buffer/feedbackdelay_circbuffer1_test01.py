# feedbackdelay_circbuffer1_test01.py
# Impulse response of a delay with feedback.
# y(n) = x(n-N) + Gfb y(n-N)
# This implementation uses a circular buffer (of minimum
# length) and one buffer index.

# Set parameters of delay system
Gfb = 0.5       # feed-back gain
N = 5           # Delay (in samples)

# Create a delay line (buffer) to store past values. Initialize to zero.
buffer_length = N
buffer = [ 0 for i in range(buffer_length) ]    

# Delay line (buffer) index
k = 0

for i in range(31):
    
    print('y({0:2d}) = {1:f}'.format(i, buffer[k]))

    # Use impulse as input signal
    if i == 0:
        input_value = 1
    else:
        input_value = 0

    # Update buffer
    buffer[k] = input_value + Gfb * buffer[k]

    # Increment buffer index
    k = k + 1
    if k == buffer_length:
        # We have reached the end of the buffer. Circle back to front.
        k = 0

