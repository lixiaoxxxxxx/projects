from stars import *
from npc import *
from datetime import datetime

def get_degree(loc1, loc2):
	y = loc2[1] - loc1[1]
	x = loc2[0] - loc1[0]
	if x == 0:
		if y > 0:
			return 90
		else:
			return 270
	degree = math.degrees(math.atan(abs(y) / abs(x)))
	if x < 0 and y > 0:
		degree = 180 - degree
	elif x < 0 and y < 0:
		degree  = 180 + degree
	elif x > 0 and y < 0:
		degree = 360 - degree
	return degree

class Game:
	def __init__(self):
		self.objects = []
		self.suns = []
		self.hero = None
		self.delay = None
		self.disdict = {}
		self.scene = 1
		self.st = None
		self.et = None

	def add_list(self, objs):
		for o in objs:
			self.objects.append(o)
	
	def set_hero(self, hero):
		self.hero = hero
		self.add(hero)
	
	def add(self, obj):
		self.objects.append(obj)
	
	def add_sun(self, s):
		self.suns.append(s)
	
	def scale(self, sf):
		for o in self.objects:
			o.scale(sf)
	
	def show(self, screen, vp, font):
		# test phase
		screen.fill((0, 0, 0))
		for o in self.objects:
			if isinstance(o, Planet):
				new_loc = (o.loc[0] - o.r + vp[0], o.loc[1] - o.r + vp[1])
			elif isinstance(o, Lucifer):
				new_loc = (o.loc[0] - o.r + vp[0], o.loc[1] - o.r + vp[1])
			else:
				new_loc = (o.loc[0] + vp[0], o.loc[1] + vp[1])
			screen.blit(o.img, new_loc)
		self.delay = (datetime.now() - self.st).seconds
		screen.blit(font.render(str(self.delay), True, (100, 200, 100)), (50, 50))
	
	def act(self, screen, vp, sf, font):
		if self.scene == 1:
			screen.blit(self.main_meun, (0, 0))
		if self.scene == 2:
			self.scale(sf)
			for o in self.objects:
				if isinstance(o, Planet):
					self.disdict[o] = o.m / (self.hero.get_dis(o)) ** 2
					o.act((0, 0))
			self.show(screen, vp, font)
			tar = max (self.disdict.items(), key = lambda x : x[1])
			star = tar[0]
			degree = 270 - get_degree(tar[0].loc, self.hero.loc)
			self.hero.set_star(degree, star)
			self.hero.act()


