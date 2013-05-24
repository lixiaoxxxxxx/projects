import pygame
from pygame.locals import *
from sys import exit
from random import *


class digit_rain(pygame.sprite.Sprite):
	
	def __init__(self, pos_x):
		pygame.sprite.Sprite.__init__(self)
		self.length = randint(30, 150)
		self.delay = randint(0, 3000)
		self.rain_drop = []
		for i in xrange(0, self.length):
			self.rain_drop.append(randint(0, 99))
		self.pos_x = pos_x
		self.pos_y = 0
		self.rain_color = []
		self.rate_R = 13
		self.rate_G = 2
		self.rate_B = 13
		self.speed = 20
		self.flag = 0
		for i in xrange(0, self.length):
			self.rain_color.append((max(0, 255 - i * self.rate_R), max(100, 255 - i * self.rate_G), max(0, 255 - i * self.rate_B)))



class rain(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.rain = []
		for i in range(0, 20):
			self.rain.append(digit_rain(i * 40))
	
	def update(self):
		for i in range(0, 20):
			if self.rain[i].flag == 1:
				self.rain[i] = digit_rain(i * 40)

#rain = []
#for i in range(0, 20):
	#rain.append(digit_rain(i * 40))

#def show(drop):
	#for i in xrange(0, drop.length):
		#screen.blit(font.render(str(drop.rain_drop[i]), True, drop.rain_color[i]), (drop.pos_x, drop.pos_y - drop.speed * i - drop.delay))
		#if drop.pos_y - drop.speed * i - drop.delay > 600 and i == drop.length - 1:
			#drop.flag = 1
	#drop.pos_y += 10

#def circulate():
	#for i in range(0, 20):
		#if rain[i].flag == 1:
			#rain[i] = digit_rain(i * 40)

#pygame.init()
#font = pygame.font.SysFont("helvetica", 15)
#screen = pygame.display.set_mode((800, 600), 0, 32)
#timer = pygame.time.Clock()

#while True:
	#for event in pygame.event.get():
		#if event.type == QUIT:
			#exit()
	#screen.fill((0, 0, 0))
	#for drop in rain:
		#show(drop)
	#circulate()
	#pygame.display.update()
	#timer.tick(30)
