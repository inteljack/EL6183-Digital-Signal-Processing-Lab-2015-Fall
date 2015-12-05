import sys
import pygame
import ezscroll
from ezscroll import N,S,E,W, ScrollBar, ScrollPane, BGCOLOR

ScrSize = (300,600)
Origin  = (0,0)
Gray    = (200,200,200)

def examples():
    """ Examples of how to use ezscroll.
    One is a scrollpane, the other is a scrollbar.
    The scrollpane handles some things like offsets,
    puts the scrollbars in a sprite group, and blits the world.
    If you just want one scrollbar, still may be easier to
    use ScrollPane and pass [S] or [E], etc.
    Closing window of proceeds through examples.
    """    
    pygame.init()
    screen = pygame.display.set_mode(ScrSize)
    world = pygame.Surface((ScrSize[0]*2, ScrSize[1]*2))
    world.fill(Gray)
    for x in xrange(100, world.get_size()[0], 200):
        for y in xrange(100, world.get_size()[1], 200):
            pygame.draw.circle(world, (225,34,43), (x,y), 100, 10)          
    bg = pygame.Surface(ScrSize).convert()
    

    # ###  EXAMPLE 1
    # bg.fill(BGCOLOR)
    # pygame.display.set_caption("Example 1:  ScrollPane")
    # initRect = pygame.Rect(screen.get_rect())
    # sp = ScrollPane(
    #     world.get_size(),
    #     initRect,
    #     world,
    #     bg,
    #     [S, W, N],
    #     3,
    #     True,
    #     20)
    # sp.draw(bg)
    # screen.blit(bg,Origin)
    # pygame.display.flip()
    # while True:
    #     event = pygame.event.wait()
    #     if event.type is pygame.QUIT: break
    #     sp.clear()
    #     sp.update(event)
    #     changes = sp.draw(bg)
    #     screen.blit(bg,Origin)
    #     pygame.display.update(changes)


    ###  EXAMPLE 2
    pygame.display.set_caption("Example 2:    ScrollBar")
    thick = 20
    scrollRect = pygame.Rect(0, 0, ScrSize[0], thick)
    excludes = ((0, thick), ScrSize) # rect where sb update is a pass
    group = pygame.sprite.RenderPlain()    
    sb = ScrollBar(
        group,
        world.get_width(),
        scrollRect,
        bg,
        0,
        excludes,
        4,
        True,
        thick,
        (170,220,180),
        (200,210,225),
        (240,240,250),
        (0,55,100))    
    sb.draw(bg)
    bg.blit(world, (0,thick),
            (sb.get_scrolled(),(ScrSize[0],ScrSize[1]-thick)))   
    screen.blit(bg, Origin)
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type is pygame.QUIT: break
        sb.update(event)
        changes = sb.draw(bg)
        if len(changes) > 0:
            changes.append(bg.blit(world, (0,thick),
                  (sb.get_scrolled(),(ScrSize[0],ScrSize[1]-thick))))
        screen.blit(bg,Origin)
        print sb.get_scrolled()
        pygame.display.update(changes)
        
##        # you can skip even sending any events in the view area       
##        try: 
##            if not sb.exclude.collidepoint(event.pos):
##                sb.update(event)
##                ...

    # ###  EXAMPLE 3
    # import random
    # pygame.display.set_caption("Example 3: ScrollBar")
    # scrollRect = pygame.Rect(0, 0, thick,ScrSize[1])
    # excludes = ((thick, 0), ScrSize) # rect where sb update is a pass
    # group = pygame.sprite.RenderPlain()
    # sb = ScrollBar(
    #     group,
    #     world.get_height(),
    #     scrollRect,
    #     bg,
    #     1,
    #     excludes,
    #     4,
    #     True,
    #     thick,
    #     (120,120,160,10),
    #     (88,57,99,214),
    #     (240,240,250,20),
    #     (0,55,100,50))  
    # sb.draw(bg)
    # bg.blit(world, (thick,0),(sb.get_scrolled(),
    #                           (ScrSize[0]-thick,ScrSize[1])))   
    # screen.blit(bg, Origin)
    # pygame.display.flip()
    # clock = pygame.time.Clock()
    # counter = 0
    # while True:
    #     counter += clock.tick()
    #     if counter > 1000: chichi = 0
    #     if counter % 100 == 0:
    #         scrollAmount = random.randrange(-20, 20, 1) 
    #         sb.scroll(scrollAmount)
    #     changes = sb.draw(bg)
    #     if len(changes) > 0:
    #         scrolled = sb.get_scrolled()
    #         changes.append(
    #             bg.blit(world, (thick,0),
    #             (scrolled[0], scrolled[1],
    #             ScrSize[0],ScrSize[1])))
    #     screen.blit(bg,Origin)
    #     pygame.display.update(changes)
    #     for event in pygame.event.get():
    #         if event.type is pygame.QUIT:
    #             pygame.quit()
    #             sys.exit(0)



if __name__ == '__main__':
    examples()