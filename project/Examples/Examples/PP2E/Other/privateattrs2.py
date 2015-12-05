class MyClass:
    def __init__(self):
        self.__attr = 21           # set a name
    def process(self):
        print self.__attr * 2      # use the name: 42

class YourClass(MyClass):          # customize process
    def __init__(self):
        MyClass.__init__(self)     # construct super
        self.attr = 'spam'         # set a name
    def process(self):
        print self.attr * 3        # use it: spamspamspam

X = YourClass()
X.process()               # spamspamspam
MyClass.process(X)        # fixed--42
