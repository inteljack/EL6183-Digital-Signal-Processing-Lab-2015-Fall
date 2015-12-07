
import struct
import math

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)


def clip16_arr( x ):
    i = 0
    k = [0.0 for n in range(0, len(x))]

    for n in x:
        if n > 32767:
            k[i] = 32767
        elif n < -32768:
            k[i] = -32768
        else:
            k[i] = n
        i = i + 1     
    return k

def clip16_warning( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
        print 'positive clipping'
    elif x < -32768:
        x = -32768
        print 'negative clipping'
    else:
        x = x        
    return int(x)
