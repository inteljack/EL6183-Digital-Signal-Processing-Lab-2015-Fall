class OperandButton(Button):
    def __init__(self, parent, text, char):
        self.text = text
        self.char = char
        Button.__init__(self, parent, text=char, command=self.press)
        self.pack(side=LEFT, expand=YES, fill=BOTH)
    def press(self):
        self.text.set( self.text.get() + self.char )     # show my char

...
for char in row: OperandButton(frm, text, char)   # in CalcGui
