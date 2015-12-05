# pygame_demo_01.py

import pygame

pygame.init()  # Initializes pygame

pge = pygame.event.get()

print pge
print type(pge)
	
print 'pygame.KEYDOWN = ', pygame.KEYDOWN
print 'pygame.KEYUP = ', pygame.KEYUP

print 'Press q to quit (quit on un-press)'

stop = False

while stop == False:

	pge = pygame.event.get()

	if len(pge) > 0:
		print ''
		print 'len(pge) = ', len(pge)

	for event in pge:

		print 'type(event) =', type(event)
		print 'event = ', event
		print 'event.type = ', event.type

		if event.type == pygame.KEYDOWN:
			print('User pressed %d key.' % event.key)

			# Check if 'q' key was pressed
			if event.key == pygame.K_q:
				stop = True

		if event.type == pygame.KEYUP:
			print('User un-pressed %d key.' % event.key)


print 'stop = ', stop

pygame.quit()

print 'end of program'

