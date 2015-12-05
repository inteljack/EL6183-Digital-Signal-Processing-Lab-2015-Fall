class ShoeSketch:                     # make a new class object
    print 'making a class...'         # printed when the class is defined
    shoeSize = 7.5                    # class data shared by all instances
    def feet(self, value = None):     # make a method function
        if not value:
            return self.numFeet       # get my feet:  x.feet() 
        else:		
            self.numFeet = value      # set my feet:  x.feet(N)
    def worth(self):
        return self.numFeet * self.shoeSize
