##############################################################################
# PyDraw-after: simple canvas paint program and object mover/animator
# use widget.after scheduled events to implement object move loops, such 
# that more than one can be in motion at once without having to use threads;
# this does moves in parallel, but seems to be slower the time.sleep version;
# see also canvasDraw in Tour: builds and passes the incX/incY list at once:
# here, would be allmoves = ([(incrX, 0)] * reptX) + ([(0, incrY)] * reptY)
##############################################################################

from movingpics import *

class MovingPicsAfter(MovingPics): 
    def doMoves(self, delay, objectId, incrX, reptX, incrY, reptY):
        if reptX:
            self.canvas.move(objectId, incrX, 0)
            reptX = reptX - 1
        else:
            self.canvas.move(objectId, 0, incrY)
            reptY = reptY - 1
        if not (reptX or reptY):
            self.moving.remove(objectId)
        else:
            self.canvas.after(delay, 
                self.doMoves, delay, objectId, incrX, reptX, incrY, reptY)
    def onMove(self, event):
        traceEvent('onMove', event, 0)
        object = self.object                      # move curr obj to click spot
        if object:
            msecs  = int(pickDelays[0] * 1000)
            parms  = 'Delay=%d msec, Units=%d' % (msecs, pickUnits[0])
            self.setTextInfo(parms)
            self.moving.append(object) 
            incrX, reptX, incrY, reptY = self.plotMoves(event)
            self.doMoves(msecs, object, incrX, reptX, incrY, reptY)
            self.where = event

if __name__ == '__main__':
    from sys import argv                          # when this file is executed
    if len(argv) == 2: 
        import movingpics                         # not this module's global
        movingpics.PicDir = argv[1]               # and from* doesn't link names
    root = Tk()
    MovingPicsAfter(root)
    root.mainloop()
