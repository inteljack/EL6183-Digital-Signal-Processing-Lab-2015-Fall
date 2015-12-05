# use threads for redraw timer
# this module customizes canvaspics.SlideShow
# note: / 1000 -> int, so 500/1000 = 0 time delay

from Tkinter import *                         
import slideShow  
import thread, random, time

class SlideShow(slideShow.SlideShow): 
    def timerThreadFunction(self):
        while self.loop:
            self.drawNext()
            time.sleep(self.msecs / 1000.0)
    def onTimer(self):
        thread.start_new_thread(self.timerThreadFunction, ())


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        picdir = sys.argv[1]
    else:
        picdir = '../gifs'

    root = Tk()
    Label(root, text="Python Slide Show Viewer, threads version").pack()
    SlideShow(root, msecs=1000, picdir=picdir, bd=3, relief=SUNKEN).pack()
    root.mainloop()
