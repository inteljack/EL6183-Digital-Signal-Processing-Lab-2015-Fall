#########################################################
# C runs Python code in this module in embedded mode.
# Such a file can be changed without changing the C layer.
# There is just standard Python code (C does conversions).
# You can also run code in standard modules like string.
#########################################################

import string

message = 'The meaning of life...'

def transform(input):
    input = string.replace(input, 'life', 'Python')
    return string.upper(input)
