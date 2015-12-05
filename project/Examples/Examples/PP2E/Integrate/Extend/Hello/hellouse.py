import hello

print hello.message('C')
print hello.message('module ' + hello.__file__)

for i in range(3):
    print hello.message(str(i))

