from config import platform

class GuiManager:
    if platform == 'unix':
        gui = 'X11'
    else:
        gui = 'Windows'

    def display(self):
        if self.gui == "X11": pass # ...etc...
