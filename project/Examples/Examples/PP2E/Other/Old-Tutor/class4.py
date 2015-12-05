class Mammal:
    def __init__(self, legs):
        self.legs = legs

class Primate(Mammal):
    def __init__(self, stance, legs):
        self.stance = stance
        Mammal.__init__(self, legs)     # call superclass init manually

class Hacker(Primate):
    def __init__(self, name):
        self.name = name
        Primate.__init__(self, 'upright', 2)
