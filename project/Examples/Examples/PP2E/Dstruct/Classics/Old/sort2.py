def sort(list, field, func = lambda x,y: x <= y):        # default: ascending 
    res = list[:0]                                       # return operand type
    for j in range(len(list)):
        i = 0
        for y in res:
            if func( list[j][field], y[field] ): break
            i = i+1
        res = res[:i] + list[j:j+1] + res[i:]            # list can be immutable
    return res 

if __name__ == '__main__':
    table = ( {'name':'doe'}, {'name':'john'} )
    print sort(table, 'name', lambda x,y: x > y)
    print sort(table, 'name', lambda x,y: x < y)
