import math
import pygame
from circular_motion import *
from pygame.locals import *

def test_img(color, r):
	s = pygame.Surface((2 * r, 2 * r))
	s.fill((0xff, 0xff, 0xff))
	pygame.draw.circle(s, color, (r, r), r)
	return s


class Space:
	def __init__(self, loc, img):
		self.loc = loc
		self.img = img
		self.x, self.y = img.get_rect().size
		self.r = 0
		self.scale_factor = 1.
	
	def scale(self, sf):
		self.scale_factor += sf
		self.img = pygame.transform.scale(self.img, (int(self.x * self.scale_factor),
			int(self.y * self.scale_factor)))


class Planet:
	def __init__(self, m, loc = (0, 0), r = 1, img = None, 
			selfd = 1, selfs = 1, planets = [],
			direction = 1, speed = 0, tag = None):
		self.tag = tag
		self.m = m
		self.r = r
		self.loc = loc
		self.origin_img = pygame.transform.scale(img, (2 * r, 2 * r))
		self.img = self.origin_img
		#self.img = test_img((100, 200, 200), r)
		self.selfd = selfd
		self.selfs = selfs
		self.twin_star = None
		self.objects = []
		self.planets = []
		self.degree = 0
		self.hero = None
		for p in planets:
			self.planets.append(p)

		self.successors = []
		for p in planets:
			for pp in p.successors:
				self.successors.append(pp)
			self.successors.append(p)

		self.direction = direction
		self.speed = speed
		self.scale_factor = 1.

	def rotate(self, degree):
		#self.degree += degree
		orig_rect = self.img.get_rect()
		#rot_image = pygame.transform.rotate(self.origin_img, self.degree)
		rot_image = pygame.transform.rotate(self.origin_img, degree)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		self.img = rot_image.subsurface(rot_rect).copy()
	
	def add(self, p):
		self.planets.append(p)
	
	def scale(self, sf):
		self.scale_factor += sf
		self.img = pygame.transform.scale(self.img, (int(2 * self.r * self.scale_factor),
			int(2 * self.r * self.scale_factor)))
	
	def move(self, mv):
		x, y = mv
		x1, y1 = self.loc
		if self.hero != None:
			self.hero.move_mv(mv)
		self.loc = (x1 + x, y1 + y)
	def self_rotate(self):
		self.rotate(self.selfd * self.degree)
		if self.hero != None:
			self.hero.loc = get_loc(self.loc, self.hero.loc, -self.selfs * self.selfd)
		self.degree += self.selfs

	def act(self, move_vector):
		#print "now in", self.tag, "with stars", len(self.successors)
		#print "mv is ", move_vector
		self.self_rotate()
		self.move(move_vector)

		for p in self.successors:
			p.move(move_vector)
		#if self.tag == 's':
			#1 / 0
		for p in self.planets:
			#print self.cal_loc(p)
			#p.loc = self.cal_loc(p)
			#print self.loc, "loc"
			#print p.speed * p.direction, "speed"
			v = vec(p.loc, get_loc(self.loc, p.loc, p.speed * p.direction))
			p.act(v)
			#print p.loc, "p.loc"

