def sort(seq, func=(lambda x,y: x <= y)):             # default: ascending
    res = seq[:0]                                     # return seq's type
    for j in range(len(seq)):
        i = 0
        for y in res:
            if func(seq[j], y): break
            i = i+1
        res = res[:i] + seq[j:j+1] + res[i:]          # seq can be immutable
    return res 

if __name__ == '__main__':
    table = ({'name':'doe'}, {'name':'john'})
    print sort(list(table),  (lambda x, y: x['name'] > y['name']))
    print sort(tuple(table), (lambda x, y: x['name'] <= y['name']))
    print sort('axbyzc')
