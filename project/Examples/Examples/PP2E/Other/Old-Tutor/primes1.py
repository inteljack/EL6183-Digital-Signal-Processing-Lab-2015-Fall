x = y / 2
while x > 1:
    if y % x == 0:			  # remainder is zero?
        print y, 'has factor', x
        break				  # skip the loop's 'else'
    x = x-1
else:					  # exited normally: no factor found		
    print y, 'is prime'
