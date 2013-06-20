import math
import pygame
from pygame.locals import *
from circular_motion import *

class Fat_Lucifer:
	def __init__(self, loc = (0, 0), r = 1, img = None):
		self.loc = loc
		self.r = r
		self.img_origin = pygame.transform.scale(img, (2 * r, 2 * r))
		self.img = self.img_origin
		self.star = None
	def get_dis(self, p):
		return ((self.loc[0] - p.loc[0]) ** 2 + (self.loc[1] - p.loc[1]) ** 2) ** 0.5

	def get_v(self):
		p = self.star
		x = math.cos(d2a(get_degree(self.loc, self.star.loc))) * p.m
		y = math.sin(d2a(get_degree(self.loc, self.star.loc))) * p.m
		print x, "x"
		print y, "y"
		self.v = (x, y)

	def act(self):
		self.get_v()
		print self.v
		self.move()

	def set_star(self, degree, star):
		self.img = pygame.transform.rotate(self.origin_img, degree)
		self.star = star

class Lucifer:
	def __init__(self, loc = (0, 0), r = 1, img_r = None, img_l = None, degree = 0):
		self.loc = loc
		self.r = r 
		self.origin_r = pygame.transform.scale(img_r, (2 * r, 2 * r))
		self.origin_l = pygame.transform.scale(img_l, (2 * r, 2 * r))
		self.face = 1
		self.img = self.origin_r
		self.degree = degree
		self.star = None
		self.f = (0, 0)
		self.mv = (0, 0)
		self.landed = False
		self.landing = False
	
	def bling(self):
		if self.star.twin_star != None:
			v = vec(self.star.loc, self.star.twin_star.loc)
			self.move_mv(v)
			self.star.hero = None
			self.star = self.star.twin_star
			self.star.hero = self
			self.landed = True
			#self.mv = (0, 0)
			return v

	def get_dis(self, p):
		return ((self.loc[0] - p.loc[0]) ** 2 + (self.loc[1] - p.loc[1]) ** 2) ** 0.5
	def get_dis_1(self, loc, p):
		return ((loc[0] - p.loc[0]) ** 2 + (loc[1] - p.loc[1]) ** 2) ** 0.5

	def scale(self, sf):
		pass

	def walk(self, direction):
		#print "walking"
		self.loc = get_loc(self.star.loc, self.loc, direction * 5)
	
	def move_mv(self, mv):
		x, y = mv
		x1, y1 = self.loc
		self.loc = (x1 + x, y1 + y)
	
	def adjusting(self):
		if self.get_dis(self.star) > self.star.r + self.r:
			xr, yr = self.loc
			fx, fy = self.f
			self.loc = (xr + 0.1 * fx, yr + 0.1 * fy)
			self.mv = (0, 0)
		else:
			self.mv = (0, 0)
			#self.f = (0, 0)
			#self.landed = True

	def move(self):
		dis = self.get_dis(self.star)
		if dis > self.star.r + 1.5 * self.r:
			self.landed = False

		if self.landed == True:
			self.adjusting()
			return
		if dis > self.star.r + self.r:
			xr, yr = self.loc
			#dx, dy = self.mv
			dx, dy = self.mv
			temp = (xr + dx, yr + dy)
			if self.get_dis_1(temp, self.star) < self.star.r + self.r:
				self.mv = (0, 0)
				self.star.hero = self
				self.landed = True
				self.adjusting()
				return
			self.loc = (xr + dx, yr + dy)
			self.landed = False
			self.star.hero = None
		elif self.landed == False:
			xr, yr = self.loc
			dx, dy = self.mv
			self.loc = (xr + dx, yr + dy)
		#else:
			##print "landed"
			#self.landed = True
			##while 1:
				##pass
	
	def jump(self):
		print "jump"
		self.landed = False
		x, y = self.f
		r = (x ** 2 + y ** 2) ** 0.5
		self.mv = (-14 * x / r, -14 * y / r)

	def rotate(self, degree):
		orig_rect = self.img.get_rect()
		#rot_image = pygame.transform.rotate(self.origin_img, self.degree)
		if self.face == 1:
			rot_image = pygame.transform.rotate(self.origin_r, degree)
		else:
			rot_image = pygame.transform.rotate(self.origin_l, degree)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		self.img = rot_image.subsurface(rot_rect).copy()


	def get_v(self):
		p = self.star
		x = math.cos(d2a(get_degree(self.loc, self.star.loc))) * p.m
		y = math.sin(d2a(get_degree(self.loc, self.star.loc))) * p.m
		#print x, "x"
		#print y, "y"
		vx, vy = self.mv
		self.f = (x, y)
		#mx, my = vx + x * 0.1, vy + y * 0.1
		#if mx ** 2 + my ** 2 > 16:
			#return
		self.mv = (vx + x * 0.1, vy + y * 0.1)

	def act(self):
		self.get_v()
		self.move()
		#print self.mv

	def set_star(self, degree, star):
		self.rotate(degree)
		self.star = star

