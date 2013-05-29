import pygame
import sys
from pygame.locals import *
from game import *

pygame.init()
screen = pygame.display.set_mode((500, 500), 0, 32)
timer = pygame.time.Clock()
FPS = 10


#p = Planet(1, (400, 300), 30, None, 1, 3, 0, 100)
#planets = []
#planets.append(p)

#s = Sun(1, (300, 300), 50, None, planets)
##s.move()

#test = pygame.Surface((100, 100))
#test.fill((0, 0, 0))

#def draw(planet):
	#new_loc = (planet.loc[0] - planet.r, planet.loc[1] - planet.r)
	#screen.blit(planet.img, new_loc)

view_point = [0, 0]

def control(ks):
	global view_point
	speed = 5
	if K_w in ks:
		view_point[1] -= speed
	if K_s in ks:
		view_point[1] += speed
	if K_a in ks:
		view_point[0] -= speed
	if K_d in ks:
		view_point[0] += speed

game = Game()
p = Planet(1, (0, 0), 10, None, speed = 3, dis = 60)
s = Planet(1, (0, 0), 30, None, planets = [p], speed = 1, dis = 150)
t  = Planet(1, (300, 300), 50, None, planets = [s])
game.add(p)
game.add(s)
game.add(t)
ks = set()

while True:
	screen.fill((0xff, 0xff, 0xff))
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN:
			ks.add(event.key)
		if event.type == KEYUP:
			ks.remove(event.key)
	print pygame.mouse.get_pos()
	game.act(screen, view_point)
	control(ks)
	pygame.display.update()
	timer.tick(FPS)
