class Scalar:
    def __add__(self, other):
        print 'Scalar.add'
    def __radd__(self, other):
        print 'Scalar.radd'

class Vector:
    def __add__(self, other):
        print 'Vector.add'
    def __radd__(self, other):
        print 'Vector.radd'

class Simple:
    pass  # no overloading

s = Scalar()
v = Vector()
o = Simple()

v + 123
123 + v        # class and non-class objects
print

s + v
v + s          # class and class, both overload +
v + v
print

v + o          # class and class, one overloads +
o + v          # same as class and non-class case


######################################################################
# C:\Stuff\Mark\Writing\PP2ndEd\dev\examples>python multioverload.py
# Vector.add
# Vector.radd
# 
# Scalar.add
# Vector.add
# Vector.add
# 
# Vector.add
# Vector.radd
######################################################################
