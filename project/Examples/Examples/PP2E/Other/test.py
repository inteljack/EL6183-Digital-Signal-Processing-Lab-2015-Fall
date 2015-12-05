def interact0():
    while 1:
        x = raw_input("Enter a number: ")
        if x == "bye": break
        print x, "squared =", atof(num) ** 2
        

def interact():
    while 1:
        try:
            x = raw_input("Enter a number: ")
            num = eval(x)                          # from string to object
            print num, "squared =", num ** 2
        except EOFError:
            print "Bye."                           # on ctrl-d
            break
        except:
            print "That's not a legal number!"
            print "enter ctrl-d to exit"           # syntax, name, overflow,...


items1 = [[1, 2, 3], [4, 5], [6, 7, 8, 9], [10]]
items2 = [[1.0, 2.0], [3.0, 4.0]]
items3 = ["spam", "ham", "eggs"]
items4 = (["a", "bc"], ["d", "efg", "h"])

def sumup(table, start=0):
    sum = start
    for row in table:
        for col in row:
            sum = sum + col
    return sum
    
print 'test is loaded...'
