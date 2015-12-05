# This file was created automatically by SWIG.
import numberc
class NumberPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            numberc.delete_Number(self.this)
    def add(self,arg0):
        val = numberc.Number_add(self.this,arg0)
        return val
    def sub(self,arg0):
        val = numberc.Number_sub(self.this,arg0)
        return val
    def display(self):
        val = numberc.Number_display(self.this)
        return val
    def __setattr__(self,name,value):
        if name == "data" :
            numberc.Number_data_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "data" : 
            return numberc.Number_data_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C Number instance>"
class Number(NumberPtr):
    def __init__(self,arg0) :
        self.this = numberc.new_Number(arg0)
        self.thisown = 1






#-------------- FUNCTION WRAPPERS ------------------



#-------------- VARIABLE WRAPPERS ------------------

