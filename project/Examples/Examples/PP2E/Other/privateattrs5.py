class Super1:
    def method(self):
        print self.compute()           # assumed to run my compute
    def compute(self):
        return 42

class Super2:
    def compute(self):                 # define my own compute
        return 'spam'

class Mixer1(Super1, Super2): pass     # Super1's compute
class Mixer2(Super2, Super1): pass     # Super2's compute

Mixer1().method()     # prints => 42
Mixer2().method()     # prints => spam

