########################################################################
# similar, but run time.sleep loops in parallel with threads, not 
# .after events or single active time.sleep loop; because threads run 
# in parallel, this also allows ovals and rectangles to be moving at 
# the _same_ time and does not require update calls to refresh the gui: 
# in fact, calling .update() can make this _crash_ today, though some 
# canvas calls seem to be thread safe or else this wouldn't work at all;
########################################################################

from Tkinter import *
import canvasDraw_tags
import thread, time

class CanvasEventsDemo(canvasDraw_tags.CanvasEventsDemo):
    def moveEm(self, tag):
        for i in range(5):
            for (diffx, diffy) in [(+20, 0), (0, +20), (-20, 0), (0, -20)]:
                self.canvas.move(tag, diffx, diffy)
                time.sleep(0.25)                      # pause this thread only
    def moveInSquares(self, tag):
        thread.start_new_thread(self.moveEm, (tag,))

if __name__ == '__main__':
    CanvasEventsDemo()
    mainloop()
