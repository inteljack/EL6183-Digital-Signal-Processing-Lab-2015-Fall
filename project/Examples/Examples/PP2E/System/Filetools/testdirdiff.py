import os
tests = ('python %s.py t1 t1', 
         'python %s.py t1 t2', 
         'python %s.py t2 t1')

expected = ''
for test in tests:
    expected = expected + os.popen(test % 'dirdiff').read()
print 'Expected:\n', expected

for altnum in range(2, 7):
    script = 'dirdiff' + str(altnum)
    output = ''
    for test in tests:
        output = output + os.popen(test % script).read()
    if output == expected:
        print script, 'passed'
    else:
        print script, 'failed:\n', output
