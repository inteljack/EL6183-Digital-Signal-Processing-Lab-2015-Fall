#! %PYTHONPATH%\python
import os
import sys
import pygame
from pygame import *

FGCOLOR = 220,220,200
BGCOLOR = 235,235,230
HICOLOR = 250,250,245
LOCOLOR = 40,40,70
N='N'
S='S'
E='E'
W='W'


class ScrollPane():
    """ Coordinates up to four scrollbars on a panel.
    Uses two ScrollBars offset, and blits world view on top.
    Use like a sprite group: update(), draw(). See examples.py
    """
    
    def __init__(
        self,
        worldSize,
        initRect,
        world,
        pane=None,
        nsew=[S,E],
        pad=0,
        pretty=False,
        thick=20,
        fgColor=FGCOLOR,
        bgColor=BGCOLOR,
        hiColor=HICOLOR,
        loColor=LOCOLOR):
        """ Figures layout and inits ScrollBars """

        self.world = world
        self.pane = pane
        self.group = pygame.sprite.RenderUpdates()
        self.nsew = nsew
        self.pad = pad
        self.thick = thick
        self.pretty = pretty
        self.fgColor = fgColor
        self.bgColor = bgColor
        self.hiColor = hiColor
        self.loColor = loColor
        
        self.viewRect = self.initViewRect(initRect, self.nsew, self.thick)
        win = self.viewRect
        self.sprites = [] # the scrollbars
        if E in self.nsew or W in self.nsew:
            scrollRect = pygame.Rect(0, win.top, initRect.width, win.height)
            exclude = win.inflate(0, self.thick).move(0,-self.thick//2)
            sb = ScrollBar(self.group, worldSize[1], scrollRect, self.pane, 1,
                    exclude, self.pad, self.pretty, self.thick,
                           fgColor, bgColor, hiColor, loColor)
            self.sprites.append(sb)

        if N in self.nsew or S in self.nsew:
            scrollRect = pygame.Rect(win.left, 0, win.width, initRect.height)
            exclude = win.inflate(self.thick, 0).move(-self.thick//2,0)
            sb = ScrollBar(self.group, worldSize[0], scrollRect, self.pane, 0,
                    exclude, self.pad, self.pretty, self.thick,
                           fgColor, bgColor, hiColor, loColor)
            self.sprites.append(sb)

##        self.clearArchive = pygame.Surface(initRect.size).convert()
##        self.clearArchive.fill((255,0,0))

    def initViewRect(self, initRect, nsew, thick):
        """ Used by init(), subtract width of scrollbars from viewable area """
        win = pygame.Rect(initRect)
        if N in nsew:
            win.top = thick
            win.height -= thick            
        if S in nsew:
            win.height -= thick         
        if E in nsew:
            win.width -= thick
        if W in nsew:
            win.left = thick
            win.width -= thick               
        return win

    def clear(self): #does nothing?
        pass # self.group.clear(self.pane, self.clearArchive)
        
    def update(self, event):
        """ Called by end user to update scroll state """
        for sb in self.sprites:
            sb.update(event)         
                
    def draw(self, surface):
        """ Called by end user to draw state to the surface """
        offsets = [0,0]
        changes = []
        for sb in self.sprites:
            offsets[sb.axis] = sb.get_scrolled()[sb.axis]
            if sb.dirty:
                changes.extend(sb.draw(surface))
        if changes:
            # Comment out this blit to see just the scrollbars.
            # To date, don't add to changes since the sb includes it.
            surface.blit(self.world, self.viewRect.topleft,
                    (offsets, self.viewRect.size))
        if self.pad and not self.pretty:
            pygame.draw.rect(
                self.pane, self.bgColor,
                self.viewRect.inflate(self.pad+1,self.pad+1), self.pad)

        return changes

    def get_pane(self):
        """ Called by end user to get the scroll pane results """
        return self.pane


class ScrollBar(pygame.sprite.DirtySprite):
    """ Same interface as sprite.Group.
    Get result of update() in pixels scrolled, from get_scrolled()
    """

    def __init__(
        self,
        group,
        worldDim,
        initRect,
        surface=None,
        axis=0,
        exclude=(0,0,0,0),
        pad=0,
        pretty=False,
        thick=20,
        fgColor=FGCOLOR,
        bgColor=BGCOLOR,
        hiColor=HICOLOR,
        loColor=LOCOLOR):

        pygame.sprite.Sprite.__init__(self,group)
        self.initTopleft = initRect.topleft
        self.exclude = pygame.Rect(exclude)
        self.image = pygame.Surface(initRect.size).convert()      
        self.rect = self.image.get_rect()
        self.surface = surface
        self.axis = axis
        self.fgColor = fgColor
        self.bgColor = bgColor
        self.hiColor = hiColor
        self.loColor = loColor        
        self.knob = pygame.Rect(self.rect)
        self.ratio = 1.0 * initRect.size[self.axis] / worldDim
        knoblist = list(self.knob.size)
        knoblist[self.axis] = (self.knob.size[self.axis] * self.ratio)
        self.knob.size = knoblist
        self.scrolling = False
        self.leftTop = [0,0]
        self.diff = [0,0]
        self.diff[self.axis] = self.initTopleft[self.axis]
        self.dirty = True
        self.pad = pad
        self.pretty = pretty
        self.thick = thick
        self.oppAxis = cmp(0,self.axis)+1
        self.prettySize = [
            self.knob.width - (pad * 2), self.knob.height - (pad * 2)]
        self.prettySize[self.oppAxis] = self.thick - (2 * pad)
 
    def update(self, event): # event must not be None
        """ Called by user with mouse events. event must not be none. """        
        if event.type is MOUSEMOTION and self.scrolling:
            self.scroll(event.rel[self.axis])
        
        elif event.type is MOUSEBUTTONDOWN and (
            self.knob.move(self.diff).collidepoint(event.pos) and not (
                    self.exclude.collidepoint(event.pos))):
            self.scrolling = True
            
        elif event.type is MOUSEBUTTONUP:
            self.scrolling = False
        
    def scroll(self, numPixels):
        """ Moves knob based on mouse events rel change along axis.
        Called internally by update(). Knob travel limited to track.
        """
        if numPixels and numPixels != 0:
            axis = self.axis
            rect = self.rect
            knob = self.knob
            knobMove = max(
                numPixels, rect.topleft[axis] - knob.topleft[axis])
            knobMove = min(
                knobMove, rect.bottomright[axis] - knob.bottomright[axis])
            knobMoves = [0,0]
            knobMoves[axis] = knobMove
            self.knob.move_ip(knobMoves)
            self.leftTop[self.axis] += knobMove / self.ratio
            self.dirty = True    

    def draw(self, surface):
        """ Blits sprite image to a surface if it exists.
        todo: Called by update()>updateViews() if self.auto is True.
        Also mimics group.draw, returning rectangle.
        """
        if  self.dirty and surface:
            self.dirty = False
            pygame.draw.rect(self.image, self.bgColor, self.rect, 0) 
            if self.pretty:
                self.drawPretty()
            else:
                pygame.draw.rect(self.image, self.fgColor, self.knob, 0)
                if self.pad:
                    pygame.draw.rect(self.image,
                                     self.bgColor, self.knob, self.pad)
            return [surface.blit(self.image, self.initTopleft)]
        else:
            return []

    def get_scrolled(self):
        """ Called by end user to get pixels scrolled,
        as result of update()
        """
        return self.leftTop

    def moveRects(self,rects,moves):
        for rect in rects:
            rect.move_ip(moves)

    def drawRects(self,rectInfo, surf):
        for item in rectInfo:
            pygame.draw.rect(surf, item[0], item[1], item[2])
            

    def drawPretty(self):

        """ Used internally. Draws drop-shadowed knob if self.pretty
        This drawing method requires the rendering of 6 rects.
        Three for each knob end, overlapping HiColor, LoColor, FgColor
        Both are drawn regardless if hidden.
        Comment out the blit of world here to see exactly.
        """
        axis = self.axis
        surf = self.image
        oppAxis = self.oppAxis
        pad = self.pad
        knob = self.knob
        psize = self.prettySize
        hiRect = pygame.Rect((knob.left + pad, knob.top + pad), psize )
        loRect = hiRect.inflate(-1,-1).move(1,1)
        fgRect = loRect.inflate(-1,-1)
        rectInfo = ((self.hiColor, hiRect, 1),
                    (self.loColor, loRect, 1),
                    (self.fgColor, fgRect, 0))       
        self.drawRects(rectInfo, surf)            
        moves = [0,0]
        moves[oppAxis] = knob.size[oppAxis] - psize[oppAxis] - (2 * pad)
        if moves[oppAxis] > 2 * self.thick: # avoid overlapping bars
            self.moveRects((hiRect, loRect, fgRect), moves)
            self.drawRects(rectInfo,surf)


        
if __name__ == '__main__':
    import examples
    examples.examples()