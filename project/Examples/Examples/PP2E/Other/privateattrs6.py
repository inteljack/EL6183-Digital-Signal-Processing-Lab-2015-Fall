class Super1:
    def method(self):
        print self.__compute()         # really run my compute
    def __compute(self):
        return 42

class Super2:
    def __compute(self):               # define my own compute
        return 'spam'

class Mixer1(Super1, Super2): pass     # Super1's compute
class Mixer2(Super2, Super1): pass     # Super1's compute too

Mixer1().method()     # prints => 42
Mixer2().method()     # prints => 42
