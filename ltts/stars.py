import math
import pygame
from pygame.locals import *

def test_img(color, r):
	s = pygame.Surface((2 * r, 2 * r))
	s.fill((0xff, 0xff, 0xff))
	pygame.draw.circle(s, color, (r, r), r)
	return s


class Planet:
	def __init__(self, m, loc = None, r = 1, img = None, 
			sd = 1, ss = 1, planets = [],
			direction = 1, speed = 0, degree = 0, dis = 0):
		self.m = m
		self.r = r
		self.loc = loc
		#self.img = img
		self.img = test_img((100, 200, 200), r)
		self.sd = sd
		self.ss = ss
		self.planets = []
		for p in planets:
			self.planets.append(p)

		self.direction = direction
		self.speed = speed
		self.degree = degree
		self.dis = dis

	def cal_loc(self, p):
		p.degree += p.direction * p.speed
		y = p.dis * math.sin((math.pi / 180) * p.degree)
		x = p.dis * math.cos((math.pi / 180) * p.degree)
		new_x = self.loc[0] + x
		new_y = self.loc[1] + y
		new_loc = (new_x, new_y)
		return new_loc
	
	def act(self):
		for p in self.planets:
			#print self.cal_loc(p)
			p.loc = self.cal_loc(p)

#class Sun:
	#def __init__(self, m, loc, r, img, planets):
		#self.m = m
		#self.r = r
		#self.loc = loc
		##self.img = img
		#self.img = test_img((100, 100, 100), r)
		#self.planets = []
		#for p in planets:
			#self.planets.append(p)

	#def cal_loc(self, p):
		#p.degree += p.direction * p.speed
		#y = p.dis * math.sin((math.pi / 180) * p.degree)
		#x = p.dis * math.cos((math.pi / 180) * p.degree)
		#new_x = self.loc[0] + x
		#new_y = self.loc[1] + y
		#new_loc = (new_x, new_y)
		#return new_loc
	
	#def move(self):
		#for p in self.planets:
			##print self.cal_loc(p)
			#p.loc = self.cal_loc(p)

	
