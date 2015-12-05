# create an array for use in demo guis

from tkFileDialog   import askopenfilename        # get standard dialogs
from tkColorChooser import askcolor               # they live in Lib/lib-tk
from tkMessageBox   import askquestion, showerror
from tkSimpleDialog import askfloat

demos = [askopenfilename, 
         askcolor,
         lambda: askquestion('Warning', 'You typed "rm *"\nContinue?'),
         lambda: showerror('Error!', "He's dead, Jim"),
         lambda: askfloat('Entry', 'Enter credit card number')]
