
def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)

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
