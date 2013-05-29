from stars import *

class Game:
	def __init__(self):
		self.objects = []

	def add_list(self, objs):
		for o in objs:
			self.objects.append(o)
	
	def add(self, obj):
		self.objects.append(obj)
	
	def show(self, screen, vp):
		# test phase
		for o in self.objects:
			if isinstance(o, Planet):
				new_loc = (o.loc[0] - o.r + vp[0], o.loc[1] - o.r + vp[1])
				screen.blit(o.img, new_loc)
	
	def act(self, screen, vp):
		for o in self.objects:
			o.act()
		self.show(screen, vp)
