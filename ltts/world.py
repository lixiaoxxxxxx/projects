import pygame
import sys
from pygame.locals import *
from game import *
from datetime import datetime

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption("Lucifer's Trip To Space")
timer = pygame.time.Clock()
font = pygame.font.Font("babybody.ttf", 50)
FPS = 20
planet_img = pygame.image.load("planet.png").convert_alpha()
black_hole_img = pygame.image.load("black_hole.png").convert_alpha()
telegate_img = pygame.image.load("telegate.png").convert_alpha()
earth_img = pygame.image.load("earth.png").convert_alpha()
bg = pygame.image.load("space.jpg")
lucifer_r = pygame.image.load("lucifer_R.png").convert_alpha()
lucifer_l = pygame.image.load("lucifer_L.png").convert_alpha()
fat_lucifer = pygame.image.load("fat_lucifer.gif").convert_alpha()
menu = pygame.image.load("menu.png").convert_alpha()
win = pygame.image.load("win.png").convert_alpha()
lose = pygame.image.load("lose.png").convert_alpha()

view_point = [0, 0]

scale_factor = 0.

def control(ks):
	global view_point, scale_factor, game
	speed = 10
	if K_w in ks:
		view_point[1] -= speed
	if K_s in ks:
		view_point[1] += speed
	if K_a in ks:
		view_point[0] -= speed
	if K_d in ks:
		view_point[0] += speed
	
	if K_b in ks:
		v = hero.bling()
		if v != None:
			x, y = v
			view_point[0] -= x
			view_point[1] -= y

	if K_q in ks:
		exit()
	if K_f in ks:
		if game.scene == 1:
			game.scene = 2
			game.st = datetime.now()
		elif game.scene == 2:
			game.scene = 1
	
	if K_z in ks:
		hero.walk(1)
		hero.face = 1

	if K_c in ks:
		hero.walk(-1)
		hero.face = -1

	if K_x in ks:
		hero.jump()
	
	if K_r in ks:
		restart()

	#if K_q in ks:
		#scale_factor = .1
	#elif K_e in ks:
		#scale_factor = -.1
	#else:
		#scale_factor = 0.


game = Game()
#p1 = Planet(4, (0, 560), 70, img = planet_img, speed = 2, tag = "p1")
#b1 = Planet(10, (530, 520), 30, img = black_hole_img, planets = [], speed = 1, tag = "b1")
#p2 = Planet(3, (500, 60), 50, img = planet_img, speed = 2, tag = "p2")
#t1 = Planet(3, (300, 820), 50, img = telegate_img, planets = [], speed = 1, tag = "bp")
#t2 = Planet(3, (1500, 360), 50, img = telegate_img, planets = [], selfd = -1, tag = "bp")
#s1 = Planet(4, (630, 220), 40, img = planet_img, planets = [], speed = 1, tag = "bp")
#p4 = Planet(7, (800, 360), 70, img = planet_img, planets = [s1], speed = 1, tag = "bp")
#p5 = Planet(8, (1100, -50), 100, img = planet_img, planets = [], selfs = 3, tag = "bp")
#end  = Planet(4, (1500, -200), 70, img = earth_img, planets = [], selfd = -1, speed = 1, tag = "end")
##ss = Planet(2, (300, 300), 30, img = planet_img, planets = [], speed = 1, tag = "s")
##ss = Planet(10, (350, 300), 30, img = planet_img, planets = [], speed = 1, tag = "s")
##t  = Planet(3, (200, 200), 70, img = planet_img, planets = [s, ss], tag = "t")
##t  = Planet(4, (200, 200), 70, img = planet_img, planets = [ss], tag = "t")
##t1  = Planet(3.1, (550, 200), 70, img = planet_img, planets = [], tag = "t1")

#hero = Fat_Lucifer((300, 100), 20, fat_lucifer)
hero = Lucifer((50, 200), 30, lucifer_r, lucifer_l)
#space = Space((-300, -300), bg)

ks = set()
def restart():
	global view_point, scale_factor, game, hero
	view_point = [0, 0]
	game = Game()
	p1 = Planet(4, (0, 560), 70, img = planet_img, speed = 2, tag = "p1")
	b1 = Planet(10, (530, 520), 30, img = black_hole_img, planets = [], speed = 1, tag = "b1")
	p2 = Planet(3, (500, 60), 50, img = planet_img, speed = 2, tag = "p2")
	t1 = Planet(3, (300, 820), 50, img = telegate_img, planets = [], speed = 1, tag = "bp")
	t2 = Planet(3, (1500, 360), 50, img = telegate_img, planets = [], selfd = -1, tag = "bp")
	s1 = Planet(4, (630, 220), 40, img = planet_img, planets = [], speed = 1, tag = "bp")
	p4 = Planet(7, (800, 360), 70, img = planet_img, planets = [s1], speed = 1, tag = "bp")
	p5 = Planet(8, (1100, -50), 100, img = planet_img, planets = [], selfs = 3, tag = "bp")
	end  = Planet(4, (1500, -200), 70, img = earth_img, planets = [], selfd = -1, speed = 1, tag = "end")
	#ss = Planet(2, (300, 300), 30, img = planet_img, planets = [], speed = 1, tag = "s")
	#ss = Planet(10, (350, 300), 30, img = planet_img, planets = [], speed = 1, tag = "s")
	#t  = Planet(3, (200, 200), 70, img = planet_img, planets = [s, ss], tag = "t")
	#t  = Planet(4, (200, 200), 70, img = planet_img, planets = [ss], tag = "t")
	#t1  = Planet(3.1, (550, 200), 70, img = planet_img, planets = [], tag = "t1")

	#hero = Fat_Lucifer((300, 100), 20, fat_lucifer)
	hero = Lucifer((50, 200), 30, lucifer_r, lucifer_l)
	space = Space((-300, -300), bg)

	t1.twin_star = t2
	t2.twin_star = t1
	game.add(space)
	game.add(p1)
	game.add(p2)
	game.add(t1)
	game.add(t2)
	game.add(p4)
	game.add(p5)
	game.add(b1)
	game.add(s1)
	game.add(end)
	game.add_sun(p1)
	game.add_sun(p2)
	game.add_sun(t1)
	game.add_sun(t2)
	game.add_sun(p4)
	game.add_sun(p5)
	game.add_sun(b1)
	game.add_sun(end)
	game.main_meun = menu
	#game.add(p)
	#game.add(s)
	#game.add(ss)
	#game.add(t)
	#game.add(t1)
	#game.add_sun(t)
	#game.add_sun(t1)
	game.set_hero(hero)
	#game.add(tt)


restart()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN:
			ks.add(event.key)
		if event.type == KEYUP:
			ks.remove(event.key)
	#print pygame.mouse.get_pos()
	#print t.loc
	game.act(screen, view_point, scale_factor, font)
	control(ks)
	if game.delay > 60:
		screen.fill((0xff, 0xff, 0xff))
		screen.blit(lose, (0, 0))
	if hero.star != None:
		if hero.star.tag == "end" and hero.landed == True:
			screen.fill((0xff, 0xff, 0xff))
			screen.blit(win, (0, 0))
	pygame.display.update()
	timer.tick(FPS)
