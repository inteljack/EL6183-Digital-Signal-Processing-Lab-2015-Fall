from sys import stdout, exit

dmenu = {'spam': lambda:stdout.write('SPAM\n'),
         'stop': exit }

lmenu = [('eggs', lambda:stdout.write('EGGS\n')),
         ('stop', lambda:1)]
