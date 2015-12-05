class FirstClass:
    def printer(self, text):
        print text

class SecondClass(FirstClass):         # SecondClass is a FirstClass
    def print_name(self):
        self.printer(self.name)		
    def set_name(self, value):
        self.name = value
