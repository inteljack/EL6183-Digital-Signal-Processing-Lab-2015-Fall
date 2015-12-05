#! %PYTHONPATH%\python
import os
import sys
import pygame
from pygame import *

ScrSize = (300,400)
Origin  = (0,0)
Gray    = (200,200,200)
Red     = (250,20,20)
Blue    = (20,20,100)
Buff    = (200,180,180)
def main():
    """ A basic example of scrollknob code inline.
        Does not use ezscroll module.
    """
    
    pygame.init()
    screen      = pygame.display.set_mode(ScrSize)
    screenRect  = screen.get_rect()
    world = pygame.Surface((ScrSize[0]*2, ScrSize[1]*2))
    world.fill(Gray)
    for x in xrange(100, world.get_size()[0], 200):
        for y in xrange(100, world.get_size()[1], 200):
            pygame.draw.circle(world, Red, (x,y), 100, 10)          

######        
    ratio       = (1.0 * screenRect.width) / world.get_width()
    scrollThick = 20
    track = pygame.Rect(screenRect.left,screenRect.bottom - scrollThick,screenRect.width,scrollThick)   
    knob        = pygame.Rect(track)  
    knob.width   = track.width * ratio
    scrolling   = False
######
    
    while 1:

            event = pygame.event.wait()
            screen.fill( (192,188,180) )

            if event.type == QUIT:
                pygame.quit()
                sys.exit()            
######            
            elif ( event.type == MOUSEMOTION and scrolling):

                if event.rel[0] != 0:
                    move = max(event.rel[0], track.left - knob.left)
                    move = min(move, track.right - knob.right)

                    if move != 0:
                        knob.move_ip((move, 0))
                            
            elif event.type == MOUSEBUTTONDOWN and knob.collidepoint(event.pos):
                scrolling = True
                    
            elif event.type == MOUSEBUTTONUP:
                scrolling = False
                
            screen.blit(world, ((knob.left / ratio) * -1 , 0))
            pygame.draw.rect(screen, Buff, track, 0 )
            pygame.draw.rect(screen, Blue, knob.inflate(0,-5), 2)
######
            
            pygame.display.flip()

### Tells what to launch in IDE and windows double click of file.
if __name__ == '__main__': main()