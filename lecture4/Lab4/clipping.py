#This clipping.py file is for setting boundaries for struct.pack and struct.unpack 
# functions so the input will not exceed maximum allowed value.
def clip8( x ):    
    # Clipping for 16 bits
    if x > 127:
        x = 255
    elif x < -128:
        x = 0
    else:
        x = x      
    return int(x)

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)

def clip32( x ):    
    # Clipping for 16 bits
    if x > 2147483647:
        x = 2147483647
    elif x < -2147483648:
        x = -2147483648
    else:
        x = x        
    return int(x)