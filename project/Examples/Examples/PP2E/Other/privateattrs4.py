class MyClass:
    def __init__(self):
        self.__attr = 21             # set a name
    def process(self):
        print self.__getIt() * 2     # 42, presumably
    def __getIt(self):
        return self.__attr           # use the name

class YourClass(MyClass):
    def __init__(self):
        MyClass.__init__(self)
        self.__attr = 'spam'
    def process(self):
        print self.__getIt() * 3     # spamspamspam
    def __getIt(self):
        return self.__attr

X = YourClass()
X.process()
MyClass.process(X)
