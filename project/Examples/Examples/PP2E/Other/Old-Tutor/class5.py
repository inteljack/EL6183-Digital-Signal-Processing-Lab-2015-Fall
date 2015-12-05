class Mammal:
    def traits(self):
        return ['live-births', 'warm-blooded']

class Cat(Mammal):
    def lifespan(self):                 # inherit below
        return (10, 30)                 # add extra behavior

class Primate(Mammal):
    def traits(self):
        return ['large-brain'] + Mammal.traits(self)      # extend below

class Hacker(Primate):
    def traits(self):
        return ['enjoys-spam']                            # over-ride below
