import pygame
import flanger
import time


pygame.init()

#####Color table#####
RED = (200,0,0)
GREEN = (0,200,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (200,200,200)

BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)

######Setup Window######
background_colour = GREY
(display_width, display_height) = (600, 600)

pygame.display.set_caption('Tutorial 1')
gameDisplay = pygame.display.set_mode((display_width, display_height))
gameDisplay.fill(background_colour)
pygame.display.flip()

def crash():
	message_display('You Crashed')

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(5)
    

def text_objects(text, font):
	textSurface = font.render(text, True, BLACK)
	return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
        	if action == "flanger":
        		flanger.flanger_effect(0.5,0.5)
        	elif action == "WahWah":
        			crash()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  button("Flanger",450,100,100,50,GREEN,BRIGHT_GREEN,"flanger")
  button("Wah Wah",450,200,100,50,RED,BRIGHT_RED,"WahWah")
  pygame.display.update()

