import pygame
from pygame.locals import *
from sys import exit
from matrix import *


class basic_object(pygame.sprite.Sprite):
	def __init__(self, mymaps, bg, pos_x = None, hp = 1):
		pygame.sprite.Sprite.__init__(self)
		self.pos_x = bg.x + pos_x
		self.hp = hp
		self.alive = 1
	
	def get_loc(self):
		return self.pos_x, self.pos_y



class flying_object(pygame.sprite.Sprite):
	def __init__(self, mymaps, bg, shooter, pos, target, power, speed):
		#---- images



		#----

		#---- positioning
		self.rect = self.image.get_rect()
		self.pos_x = shooter.pos_x + shooter.direction * shooter.size[1]
		self.pos_y = shooter.y + shooter.gun_pos
		self.tar_x = target.rect.center[0]
		self.tar_y = target.rect.center[1]
		self.tan = 0.
		self.speed = speed
		self.d_x = self.speed * self.cal(self.tar_x - self.pos_x, self.tar_y - self.pos_y)
		self.d_y = self.d_x * self.tan

	def __del__(self):
		pass

	def cal(self, x, y):
		self.tan = float(y) / x
		cos = 1 / (1 + tan ** 2) ** 1/2
		return cos
	
	def update(self, mymaps, bg, target, flying_objects):
		self.pos_x += self.d_x
		self.pos_y += slef.d_y
		self.rect.topleft = (self.pos_x, self.pos_y)
		if pygame.sprite.collide_rect(self, target):
			target.hp -= self.power
			self.remove(flying_objects)

	




class Mymap(pygame.sprite.Sprite):
	def __init__(self, bg):
		pygame.sprite.Sprite.__init__(self)
		self.size = bg.image.get_rect().size
		self.ground = []
		for i in range(0, self.size[0]):
			if i < 40:
				self.ground.append(100)
			elif i > 1400 and i < 1580:
				self.ground.append(280)
			elif i > 1850 and i < 2000:
				self.ground.append(600 + 300)
			elif i > 2460 and i < 2880:
				self.ground.append(600 + 300)
			elif i > 4480 - 110 and i < 4520 - 110:
				self.ground.append(100)
			elif i > self.size[0] - 100:
				self.ground.append(100)
			else:
				self.ground.append(400)



class Bullet(pygame.sprite.Sprite):
	global game
	def __init__(self):
		self.start_point = game.Lucifer.x - game.bg.x
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("bullet.png").convert_alpha()
		self.y = game.Lucifer.y + 110
		self.dis = 0
		if game.Lucifer.direction == "left":
			self.x = self.start_point
			self.direction = -1
		else: 
			self.start_point = self.start_point + 100
			self.x = self.start_point
			self.direction = 1
		self.rect = self.image.get_rect()
		self.alive = 1
	def update(self):
		self.dis += 20
		self.x = game.bg.x + self.start_point + self.direction * self.dis
		self.rect.topleft = (self.x, self.y)
	def __del__(self):
		pass
		


class background:
	global game
	def __init__(self):
		self.image = pygame.image.load("demo_background.png").convert_alpha()
		#self.image = pygame.image.load("sbbg.JPG").convert()
		self.x = -150
		self.y = 0
		self.v = 0.
		self.MAX_v = 12.
		self.acceleration = 3.
		self.fraction = 1.
		self.direction = 1
		self.last_v = 0
	def loc(self):
		return (self.x, self.y)
	def moving(self):
		if self.v != 0:
			return 1
		else:
			return 0 

	def move(self, pressed = 0):
		if game.Lucifer.dis == 0:
			flag = 1
		else:
			flag = 0
		if self.v > self.MAX_v:
			self.v = self.MAX_v
		if self.v < -self.MAX_v:
			self.v = -self.MAX_v
		if self.v >= 0:
			self.v += (pressed) * self.acceleration - flag * self.moving() * self.fraction
		if self.v < 0:
			self.v += (pressed) * self.acceleration + flag * self.moving() * self.fraction

		if self.v * self.last_v < 0:
			self.v = 0
		self.x += self.v
		self.last_v = self.v

	def toright(self, speed = 10):
		self.x -= speed
	def toleft(self, speed = 10):
		self.x += speed
	def getloc(self):
		return (self.x, self.y)


class Dragon(basic_object):
	global game
	#	width: 100 height: 130
	def __init__(self, mymaps, bg, pos_x, hp):

		self.dragon_1 = pygame.transform.scale(pygame.image.load("dragon_1.png").convert_alpha(), (500, 500))
		self.dragon_2 = pygame.transform.scale(pygame.image.load("dragon_2.png").convert_alpha(), (500, 500))
		self.dragon_3 = pygame.transform.scale(pygame.image.load("dragon_3.png").convert_alpha(), (500, 500))
		self.dragon_dead = pygame.transform.scale(pygame.image.load("dragon_dead.png").convert_alpha(), (500, 500))
		basic_object.__init__(self, mymaps, bg, pos_x, hp)
		self.image = self.dragon_2
		self.rect = self.image.get_rect()
		self.size = self.rect.size
		#self.pos_y = mymaps[0].ground[pos_x] - self.size[1]
		self.pos_y = 30
		self.rect.topleft = (self.pos_x, self.pos_y)
		self.step = 0
		self.dying = 18
		self.dead = 0
		self.alive = 1
	
	#def get_loc(self):
		#return self.pos_x, self.pos_y

	def __del__(self):
		pass
	
	
	def die(self):
		self.pos_x = game.bg.x + 2500
		self.rect.topleft = (self.pos_x, self.pos_y)
		if self.dying != 0:
			self.image = self.dragon_dead
			self.pos_y += 20
		else:
			self.dead = 1
		self.dying -= 1
	
	def update(self):
		self.pos_x = game.bg.x + 2500
		self.rect.topleft = (self.pos_x, self.pos_y)
		if self.alive == 0:
			self.die()
			return

		if pygame.sprite.collide_rect(self, game.Lucifer) == 1:
			if game.Lucifer.protected_count == 0:
				game.Lucifer.hp -= 10
				game.Lucifer.protected_count = 30

		for b in game.bullets:
			if pygame.sprite.collide_rect(self, b) == 1:
				self.hp -= 1
				if self.hp == 0:
					self.alive = 0
				b.__del__()
				game.bullets.remove(b)
		self.step += 1
		if self.step < 5:
			self.image = self.dragon_2
		elif self.step < 10:
			self.image = self.dragon_1
		elif self.step < 15:
			self.image = self.dragon_2
		elif self.step < 20:
			self.image = self.dragon_3
		else:
			self.step = 0


class Monster_1(basic_object):
	global game
	#	width: 100 height: 130
	def __init__(self, mymaps, bg, pos_x, hp):

		self.walk1_r = pygame.image.load("Monster1_right_1.png").convert_alpha()
		self.walk1_l = pygame.image.load("Monster1_left_1.png").convert_alpha()
		self.walk2_r = pygame.image.load("Monster1_right_2.png").convert_alpha()
		self.walk2_l = pygame.image.load("Monster1_left_2.png").convert_alpha()
		self.dying1 = pygame.image.load("Monster1_dying_1.png").convert_alpha()
		self.dying2 = pygame.image.load("Monster1_dying_2.png").convert_alpha()
		self.dead_left = pygame.image.load("Monster1_dead_left.png").convert_alpha()
		self.dead_right = pygame.image.load("Monster1_dead_right.png").convert_alpha()
		basic_object.__init__(self, mymaps, bg, pos_x, hp)
		self.image = self.walk1_l
		self.start_point = self.pos_x
		self.rect = self.image.get_rect()
		self.size = self.rect.size
		self.pos_y = mymaps[0].ground[pos_x] - self.size[1]
		self.rect.topleft = (self.pos_x, self.pos_y)
		self.step = 0
		self.direction = -1
		self.state = "toleft"
		self.state_time = 0
		self.speed = 5
		self.dis = 0
		self.dying = 18
		self.dead = 0

	def __del__(self):
		pass
	
	def toright(self):
		self.direction = 1
		if self.step == 6:
			self.step = 0
		if self.step >= 0 and self.step < 3:
			self.image = self.walk1_r
		if self.step >= 3:
			self.image = self.walk2_r
		self.step += 1

	def toleft(self):
		self.direction = -1
		if self.step == 6:
			self.step = 0
		if self.step >= 0 and self.step < 3:
			self.image = self.walk1_l
		if self.step >= 3:
			self.image = self.walk2_l
		self.step += 1

	def change_state(self):
		if self.state == "toleft":
			self.state = "toright"
			return
		if self.state == "toright":
			self.state = "toleft"
			return
	
	def die(self):
		self.pos_x = 400 + game.bg.x + self.start_point + self.direction * self.dis
		self.rect.topleft = (self.pos_x, self.pos_y)
		if self.dying == 0:
			self.__del__()
			self.dead = 1
		if self.dying > 3:
			if self.dying % 2 == 0:
				self.image = self.dying1
			else:
				self.image = self.dying2
		else:
			if self.direction == 1:
				self.image = self.dead_right
			if self.direction == -1:
				self.image = self.dead_left
		self.dying -= 1
	
	def update(self):
		if self.alive == 0:
			self.die()
			return
		
		if pygame.sprite.collide_rect(self, game.Lucifer) == 1:
			if game.Lucifer.protected_count == 0:
				game.Lucifer.hp -= 10
				game.Lucifer.protected_count = 30


		for b in game.bullets:
			if pygame.sprite.collide_rect(self, b) == 1:
				self.alive = 0
				self.die()
				b.__del__()
				game.bullets.remove(b)

		self.dis += 5
		self.pos_x = 400 + game.bg.x + self.start_point + self.direction * self.dis
		self.rect.topleft = (self.pos_x, self.pos_y)
		if self.state == "toleft":
			self.toleft()
		if self.state == "toright":
			self.toright()
		self.state_time += 1
		if self.state_time == 25:
			self.start_point = self.start_point + self.dis * self.direction
			self.dis = 0
			self.change_state()
			self.state_time = 0

class VIM_falling_star(pygame.sprite.Sprite):
	global game
	def __init__(self, target = None, power = 10, pos = 0):
		pygame.sprite.Sprite.__init__(self)
		self.falling = pygame.image.load("star.png").convert_alpha()
		self.boom1 = pygame.image.load("boom1.png").convert_alpha()
		self.boom2 = pygame.image.load("boom2.png").convert_alpha()
		self.boom3 = pygame.image.load("boom3.png").convert_alpha()
		self.boom4 = pygame.image.load("boom4.png").convert_alpha()
		self.boom5 = pygame.image.load("boom5.png").convert_alpha()
		self.image = self.falling
		self.rect = self.image.get_rect()
		self.size = self.rect.size
		if target != None:
			self.start_x = target.pos
			self.bomb_type = 0
		else:
			self.start_x = pos
			self.bomb_type = 1
		self.pos_x = self.start_x
		self.pos_y = -self.size[1]
		self.rect.topleft = (self.pos_x, self.pos_y)
		self.boom_count = 0
		self.alive = 1
		self.current_pos = (0, 0)
	
	def boom(self):
		self.pos_x = game.bg.x + self.start_x
		self.boom_count += 1
		if self.boom_count <= 3:
			self.image = pygame.transform.scale(self.boom1, (100, int(float(self.boom1.get_rect().size[1]) / self.boom1.get_rect().size[0] * 100)))
			self.rect.topleft = (self.pos_x, self.pos_y + 120)
			self.current_pos = self.rect.topleft
		elif self.boom_count <= 6:
			self.image = pygame.transform.scale(self.boom2, (100, int(float(self.boom2.get_rect().size[1]) / self.boom2.get_rect().size[0] * 100)))
			self.rect.topleft = (self.pos_x, self.pos_y + 150)
			self.current_pos = self.rect.topleft
		elif self.boom_count <= 9:
			self.image = pygame.transform.scale(self.boom3, (100, int(float(self.boom3.get_rect().size[1]) / self.boom3.get_rect().size[0] * 100)))
			self.rect.topleft = (self.pos_x, self.pos_y + 120)
			self.current_pos = self.rect.topleft
		elif self.boom_count <= 12:
			self.image = pygame.transform.scale(self.boom4, (100, int(float(self.boom4.get_rect().size[1]) / self.boom4.get_rect().size[0] * 80)))
			self.rect.topleft = (self.pos_x, self.pos_y + 100)
			self.current_pos = self.rect.topleft
		else:
			self.image = pygame.transform.scale(self.boom5, (100, int(float(self.boom5.get_rect().size[1]) / self.boom5.get_rect().size[0] * 100)))
			self.rect.topleft = (self.pos_x, self.pos_y + 80)
			self.current_pos = self.rect.topleft
		if self.boom_count == 20:
			game.VIM.stars.remove(self)
	
	def update(self, target):
	
		if self.alive == 0:
			self.boom()
			return
		self.pos_y += 10
		self.pos_x = game.bg.x + self.start_x
		self.rect.topleft = (self.pos_x, self.pos_y)
		#print self.pos_x
		if self.pos_y + self.size[1] > target.y and self.rect.centerx - game.bg.x > target.pos and self.rect.centerx - game.bg.x < target.pos + 110:
			print "hit!"
			if target.protected_count == 0:
				if target.hp > 20:
					target.hp -= 10
					target.protected_count = 30
			self.alive = 0
		elif self.pos_y + self.size[1] > 400:
			print "ground"
			if self.rect.centerx - game.bg.x > 3530 and self.rect.centerx - game.bg.x < 3650:
				if self.bomb_type == 0:
					game.VIM.move(1)
			elif self.rect.centerx - game.bg.x > 3650 and self.rect.centerx - game.bg.x < 3760:
				if self.bomb_type == 0:
					game.VIM.move(2)
			elif self.rect.centerx - game.bg.x > 3765 and self.rect.centerx - game.bg.x < 3870:
				if self.bomb_type == 0:
					game.VIM.move(3)
			elif self.rect.centerx - game.bg.x > 3870 and self.rect.centerx - game.bg.x < 4000:
				if self.bomb_type == 0:
					game.VIM.move(4)
			elif self.rect.centerx - game.bg.x > 4000 and self.rect.centerx - game.bg.x < 4100:
				if self.bomb_type == 0:
					game.VIM.move(1)
			elif self.rect.centerx - game.bg.x > 4100 and self.rect.centerx - game.bg.x < 4200:
				if self.bomb_type == 0:
					game.VIM.move(2)
			elif self.rect.centerx - game.bg.x > 4200 and self.rect.centerx - game.bg.x < 4310:
				if self.bomb_type == 0:
					game.VIM.move(3)
			elif self.rect.centerx - game.bg.x > 4320 and self.rect.centerx - game.bg.x < 4430:
				if self.bomb_type == 0:
					game.VIM.move(4)
			self.alive = 0



class Boss1(basic_object):
	global game
	def __init__(self, mymaps, bg, pos_x, hp):
		#---- images


		#----

		#---- positioning
		basic_object.__init__(self, mymaps, bg, pos_x, hp)
		self.left = pygame.transform.scale(pygame.image.load("vim_L.png").convert_alpha(), (int(200 / 1.5), int(350 / 1.5)))
		self.right = pygame.transform.scale(pygame.image.load("vim_R.png").convert_alpha(), (int(200 / 1.5), int(350 / 1.5)))
		self.dead_1 = pygame.transform.scale(pygame.image.load("vim_dead_1.png").convert_alpha(), (int(200 / 1.5), int(350 / 1.5)))
		self.dead_2 = pygame.transform.scale(pygame.image.load("vim_dead_2.png").convert_alpha(), (int(200 / 1.5), int(350 / 1.5)))
		self.dead_3 = pygame.transform.scale(pygame.image.load("vim_dead_3.png").convert_alpha(), (int(200 / 1.5), int(350 / 1.5)))
		self.dead_4 = pygame.transform.scale(pygame.image.load("vim_dead_4.png").convert_alpha(), (int(200 / 1.5), int(350 / 1.5)))
		self.dead_5 = pygame.transform.scale(pygame.image.load("vim_dead_5.png").convert_alpha(), (int(200 / 1.5), int(350 / 1.5)))
		self.image = self.left
		self.rect = self.image.get_rect()
		self.size = self.rect.size
		self.pos_y = mymaps[0].ground[pos_x] - self.size[1]
		self.pos_x = 0
		self.hp_grid = (104, 30)
		self.hp_grid_bar = (self.hp, 26)
		self.d_x = 0
		self.d_y = 0
		self.move_count = 0
		self.flag = 0
		self.alive = 1
		self.spell_cooldown = 0
		self.dead_count = 50
		self.dead = 0
		#----
		
		#---- charachter settings
		self.stars = pygame.sprite.Group()
		self.attack_cooldown = 0
	
	def dialog(self):
		if self.hp < 90 and self.hp > 85:
			for i in range(0, 100):
				img = pygame.image.load("roar_1.png").convert_alpha()
				game.screen.blit(img, (200, 250))
				pygame.display.update()
			self.hp -= 10
		if self.hp < 70 and self.hp > 65:
			for i in range(0, 100):
				img = pygame.image.load("roar_2.png").convert_alpha()
				game.screen.blit(img, (200, 250))
				pygame.display.update()
			self.hp -= 10
		if self.hp < 30 and self.hp > 25:
			for i in range(0, 100):
				img = pygame.image.load("roar_3.png").convert_alpha()
				game.screen.blit(img, (200, 250))
				pygame.display.update()
			self.hp -= 10
		if self.hp <= 5 and self.hp > 0:
			for i in range(0, 100):
				img = pygame.image.load("roar_4.png").convert_alpha()
				game.screen.blit(img, (200, 250))
				pygame.display.update()
			self.hp -= 10

	def spot_target(self):
		if game.Lucifer.pos > 3530:
			#print "spotted"
			for x in range(3500, 3530):
				game.mymaps[0].ground[x] = 100
			return True
		else:
			return False
	
	def moving(self):
		if self.flag == 1:
			self.move_count += 1
			self.d_x -= 5
			if self.d_x < -460:
				self.d_x = -460
			if self.move_count == 40:
				self.move_count = 0
				self.flag = 0
		
		elif self.flag == 2:
			self.d_y += 2
			if self.d_y > 0:
				self.d_y = 0
			if self.move_count == 40:
				self.move_count = 0
				self.flag = 0

		elif self.flag == 3:
			self.d_y -= 2
			if self.d_y < -170:
				self.d_y = -170
			if self.move_count == 40:
				self.move_count = 0
				self.flag = 0

		elif self.flag == 4:
			self.move_count += 1
			self.d_x += 5
			if self.d_x > 340:
				self.d_x = 340
			if self.move_count == 40:
				self.move_count = 0
				self.flag = 0

	def move(self, direction):
		print "asdasd", self.pos_x - game.bg.x
		print "place", direction
		if direction == 1:
			self.flag = 1
		elif direction == 2:
			self.flag = 2
		elif direction == 3:
			self.flag = 3
		elif direction == 4:
			self.flag = 4
		
		self.rect.topleft = (self.pos_x, self.pos_y)

	def attack(self):
		if self.attack_cooldown == 50:
		#print "attacked"
			self.stars.add(VIM_falling_star(game.Lucifer, 10))
			self.attack_cooldown = 0
		if self.spell_cooldown >= 100:
			if (self.spell_cooldown - 100) % 10 == 0:
				self.stars.add(VIM_falling_star(None, 10, 3530 + ((self.spell_cooldown - 100) / 10) * 100))
			if self.spell_cooldown == 180:
				self.spell_cooldown = 0
	
	def die(self):
		self.stars = pygame.sprite.Group()
		self.dead_count -= 1
		self.pos_x = game.bg.x + 4000
		self.rect.topleft = (self.pos_x + self.d_x, self.pos_y + self.d_y)
		if self.dead_count > 40:
			self.image = self.dead_1
		elif self.dead_count > 30:
			self.image = self.dead_2
		elif self.dead_count > 20:
			self.image = self.dead_3
		elif self.dead_count > 10:
			self.image = self.dead_4
		else:
			self.image = self.dead_5
		if self.dead_count <= 0:
			self.dead = 1
			for i in range(4480 - 110, 4521 - 110):
				game.mymaps[0].ground[i] = 400
			for x in range(3500, 3530):
				game.mymaps[0].ground[x] = 400
			game.changeable_objects.remove(game.door_closed)
			game.changeable_objects.add(game.door_opened)
			game.objects.remove(self)

		
			


	def update(self):
		self.hp_grid_bar = (self.hp, 26)
		if self.hp <= 0:
			self.alive = 0
		if self.alive == 0:
			self.die()
			return
		self.moving()
		for s in game.VIM.stars:
			s.update(game.Lucifer)
		#print self.attack_cooldown
		#print len(self.stars)
		#print self.hp
		if self.spot_target() == True:
			self.spell_cooldown += 1
			self.attack_cooldown += 1
			self.attack()
			pygame.draw.rect(game.screen, (100, 100, 150), ((350, 20), self.hp_grid), 0)
			pygame.draw.rect(game.screen, (0, 200, 150), ((352, 22), self.hp_grid_bar), 0)
		self.pos_x = game.bg.x + 4000
		self.rect.topleft = (self.pos_x + self.d_x, self.pos_y + self.d_y)
		if self.pos_x + self.d_x < game.Lucifer.pos + game.bg.x:
			self.image = self.right
		else:
			self.image = self.left

		if pygame.sprite.collide_rect(self, game.Lucifer) == 1:
			if game.Lucifer.protected_count == 0:
				if game.Lucifer.hp > 20:
					game.Lucifer.hp -= 10
					game.Lucifer.protected_count = 30

		for b in game.bullets:
			if pygame.sprite.collide_rect(self, b) == 1:
				self.hp -= 3
				b.__del__()
				game.bullets.remove(b)
		





class lucifer(pygame.sprite.Sprite):
	global game
	#	width 110   height 210
	def __init__(self, bg, mymaps):
		pygame.sprite.Sprite.__init__(self)
		#self.add()
		#print self.groups()
		self.stand_l = pygame.image.load("Lucifer_stand_L.png").convert_alpha()
		self.stand_r = pygame.image.load("Lucifer_stand_R.png").convert_alpha()
		self.walk1_l = pygame.image.load("Lucifer_walk1_L.png").convert_alpha()
		self.walk1_r = pygame.image.load("Lucifer_walk1_R.png").convert_alpha()
		self.walk2_l = pygame.image.load("Lucifer_walk2_L.png").convert_alpha()
		self.walk2_r = pygame.image.load("Lucifer_walk2_R.png").convert_alpha()
		#self.bling = pygame.image.load("bling.png").convert_alpha()
		self.protected_count = 20
		self.alive = 1
		self.image = self.stand_r
		self.rect = self.image.get_rect()
		self.fire_cooldown = 5
		self.fire_cooldown_cnt = 0
		self.MAX_BULLET = 10
		self.bling_cooldown = 30
		self.bling_cooldown_grid = (94, 30)
		self.bling_cooldown_bar = (self.bling_cooldown * 3, 26)
		self.hp = 100			# for test only
		self.hp_grid = (104, 30)
		self.hp_grid_bar = (self.hp, 26)
		self.vx = 0
		self.vy = 0
		self.x = 300
		self.pos = self.x - bg.x
		self.y = mymaps[0].ground[self.x - bg.x] - self.rect.size[1]
		self.rect.topleft = (self.x, self.y)
		self.acceleration = 3.
		self.dis = 0
		self.direction = "right"
		self.step = 0
		self.level_1_final = pygame.image.load("level_1_final.png").convert_alpha()
		self.level_2_final = pygame.image.load("level_2_final.png").convert_alpha()
		self.level_3_final = pygame.image.load("level_3_final.png").convert_alpha()
		self.level_4_final = pygame.image.load("level_4_final.png").convert_alpha()

		self.haskey_1 = 0
		self.level_1 = 0
		self.showflag = 0
		
		#self.jump = 0
		#self.jump_count = 0



	def __del__(self):
		pass

	def wall_detect(self):
		if self.direction == "right":
			ground = game.mymaps[0].ground[int(self.pos + 15)]
			self.temp_dis = ground - (self.y + self.rect.size[1])
			if game.mymaps[0].ground[int(self.pos + 15)] < game.mymaps[0].ground[int(self.pos)]and self.temp_dis < 0:
				print "wall!"
				game.bg.v = 0
				return "right"
		else:
			ground = game.mymaps[0].ground[int(self.pos - 15)]
			self.temp_dis = ground - (self.y + self.rect.size[1])
			if game.mymaps[0].ground[int(self.pos - 15)] < game.mymaps[0].ground[int(self.pos)]and self.temp_dis < 0:
				print "wall!"
				game.bg.v = 0
				return "left"
		return None

	def get_loc(self):
		return(self.x, self.y)

	def toright(self):
		self.direction = "right"
		if self.dis != 0:
			self.image = self.walk2_r
		else:
			if self.step == 12:
				self.step = 0
			if self.step >= 0 and self.step < 3:
				self.image = self.stand_r
			if self.step >= 3 and self.step < 6:
				self.image = self.walk1_r
			if self.step >= 6 and self.step < 9:
				self.image = self.stand_r
			if self.step >= 9:
				self.image = self.walk2_r
			self.step += 1

	def toleft(self):
		self.direction = "left"
		if self.dis != 0:
			self.image = self.walk2_l
		else:
			if self.step == 12:
				self.step = 0
			if self.step >= 0 and self.step < 3:
				self.image = self.stand_l
			if self.step >= 3 and self.step < 6:
				self.image = self.walk1_l
			if self.step >= 6 and self.step < 9:
				self.image = self.stand_l
			if self.step >= 9:
				self.image = self.walk2_l
			self.step += 1
	def stand(self):
		self.step = 0
		if self.direction == "right":
			self.image = self.stand_r

		if self.direction == "left":
			self.image = self.stand_l
	
	def move(self):
		ground = game.mymaps[0].ground[int(self.x - game.bg.x)]
		if self.rect.bottom > 600:
			game.Lucifer.hp = 0
			print "die!!!"
		self.vy = self.vy - self.acceleration
		self.y -= self.vy
		self.dis = ground - (self.y + self.rect.size[1])
		if self.dis < 0:
			self.dis = 0
			self.y = ground - self.rect.size[1]
			self.vy = 0
		#self.dis = 400 - self.y
		#if self.y + self.rect.size[1] < 400:
			#self.vy = self.vy - self.acceleration
			#self.y -= self.dis
			#self.dis = 400 - self.y
		#else:
			#self.dis = 0
			#self.y = 400 - self.rect.size[1]
			#self.vy = 0

	def Jump(self):
		#if self.jump is 1:
			#self.jump_count += 1
			#if self.jump_count <= 10:
				#self.y -= 0.3* (10 - self.jump_count) ** 2 + 3
			#if self.jump_count > 10:
				#self.y += 0.3* (10 - self.jump_count) ** 2 + 3
			#if self.jump_count == 20:
				#self.y = 200
				#self.jump_count = 0
				#self.jump = 0
		self.vy = 30
	
	def Bling(self):
		if self.bling_cooldown == 30:
			for i in range(0, 10):
				pygame.time.Clock().tick(30)

				if self.direction == "right":
					ground = game.mymaps[0].ground[int(self.x - game.bg.x) + 30]
					self.dis = ground - (self.y + self.rect.size[1])
					if self.dis < 0:
						break
					game.bg.toright(30)
					game.screen.blit(game.bg.image, game.bg.getloc())
					game.screen.blit(self.image, self.get_loc())
					pygame.draw.rect(game.screen, (100, 100, 150), 
							((650, 20), game.Lucifer.bling_cooldown_grid), 0)
					pygame.draw.rect(game.screen, (200, 100, 150), 
							((652, 22), game.Lucifer.bling_cooldown_bar), 0)
					pygame.draw.rect(game.screen, (100, 100, 150), ((200, 20), game.Lucifer.hp_grid), 0)
					pygame.draw.rect(game.screen, (0, 200, 150), ((202, 22), game.Lucifer.hp_grid_bar), 0)
					if game.M1.alive == 1:
						game.screen.blit(game.M1.image, (game.M1.pos_x - i * 30, game.M1.pos_y))
					if game.VIM.dead == 0:
						game.screen.blit(game.VIM.image, (game.VIM.pos_x + game.VIM.d_x - i * 30, game.VIM.pos_y + game.VIM.d_y))
					game.screen.blit(game.D1.image, (game.D1.pos_x - i * 30, game.D1.pos_y))
					for s in game.VIM.stars:
						screen.blit(s.image, (s.current_pos[0] - i * 30, s.current_pos[1]))

					#hints.draw(screen)
					game.hints.update()
					for h in game.hints:
						screen.blit(h.image, (h.rect.topleft[0] - i * 30, h.rect.topleft[1]))
					game.environment_objects.draw(screen)
					pygame.display.update()
				if self.direction == "left":
					ground = game.mymaps[0].ground[int(self.x - game.bg.x) - 30]
					self.dis = ground - (self.y + self.rect.size[1])
					if self.dis < 0:
						break
					game.bg.toleft(30)
					game.screen.blit(game.bg.image, game.bg.getloc())
					game.screen.blit(self.image, self.get_loc())
					pygame.draw.rect(game.screen, (100, 100, 150), 
							((650, 20), game.Lucifer.bling_cooldown_grid), 0)
					pygame.draw.rect(game.screen, (200, 100, 150), 
							((652, 22), game.Lucifer.bling_cooldown_bar), 0)
					pygame.draw.rect(game.screen, (100, 100, 150), ((200, 20), game.Lucifer.hp_grid), 0)
					pygame.draw.rect(game.screen, (0, 200, 150), ((202, 22), game.Lucifer.hp_grid_bar), 0)
					if game.M1.alive == 1:
						game.screen.blit(game.M1.image, (game.M1.pos_x + i * 30, game.M1.pos_y))
					if game.VIM.dead == 0:
						game.screen.blit(game.VIM.image, (game.VIM.pos_x + game.VIM.d_x + i * 30, game.VIM.pos_y + game.VIM.d_y))

					game.screen.blit(game.D1.image, (game.D1.pos_x + i * 30, game.D1.pos_y))
					for s in game.VIM.stars:
						screen.blit(s.image, (s.current_pos[0] + i * 30, s.current_pos[1]))
					#hints.draw(screen)
					game.hints.update()
					for h in game.hints:
						screen.blit(h.image, (h.rect.topleft[0] + i * 30 - 300, h.rect.topleft[1]))
					game.environment_objects.draw(screen)
					pygame.display.update()
			self.bling_cooldown = 0
	def Fire(self):
		game.bullets.append(Bullet())
	
	def find_key(self):
		if self.haskey_1 == 0:
			if pygame.mouse.get_pressed() == (1, 0, 0):
				mouse_pos = pygame.mouse.get_pos()
				if mouse_pos[0] > game.Lucifer.x and mouse_pos[0] < game.Lucifer.x + 110 and mouse_pos[1] > game.Lucifer.y and mouse_pos[1] < game.Lucifer.y + 100:
					print "asdasdasdasd"
					key_img = pygame.transform.scale(pygame.image.load("key.png").convert_alpha(), (200, 100))
					for i in range(0, 100):
						game.screen.blit(key_img, (300, 200))
						pygame.display.update()
					self.haskey_1 = 1
			if K_f in game.key_set:
				key_img = pygame.transform.scale(pygame.image.load("key.png").convert_alpha(), (200, 100))
				for i in range(0, 100):
					game.screen.blit(key_img, (300, 200))
					pygame.display.update()
				self.haskey_1 = 1


	def update(self):
		if self.haskey_1 == 1:
			if pygame.sprite.collide_rect(self, game.box_closed) == 1:
				game.changeable_objects.remove(game.box_closed)
				game.changeable_objects.add(game.box_opened)
				self.showflag = 1

		if game.VIM.alive == 0:
			self.find_key()
		self.protected_count = max(0, self.protected_count - 1)
		self.pos = self.x - game.bg.x
		self.rect.topleft = (self.x, self.y)
		self.fire_cooldown_cnt = min(self.fire_cooldown_cnt + 1, self.fire_cooldown)
		self.bling_cooldown_bar = (self.bling_cooldown * 3, 26)
		self.hp_grid_bar = (self.hp, 26)
		if self.hp <= 0:
			return
		self.move()
		if self.bling_cooldown < 30:
			self.bling_cooldown += 1

		if K_q in game.key_set:
			exit()

		if K_j in game.key_set:
			if self.fire_cooldown_cnt == self.fire_cooldown and len(game.bullets) < self.MAX_BULLET:
				self.Fire()
				self.fire_cooldown_cnt = 0
		if K_l in game.key_set:
			self.Bling()
		if K_k in game.key_set and self.dis == 0:
			self.Jump()
		if K_d not in game.key_set and K_a not in game.key_set:
			self.stand()
		if K_g in game.key_set:
			game.bg.toleft(1)
		if K_h in game.key_set:
			game.bg.toright(1)
		if K_d in game.key_set:
			if self.wall_detect() != "right":
				self.toright()
				game.bg.move(-1)
		elif K_a in game.key_set:
			if self.wall_detect() != "left":
				self.toleft()
				game.bg.move(+1)
		else:
			if self.wall_detect() == None:
				game.bg.move()

class hint(pygame.sprite.Sprite):
	global game
	def __init__(self, image_file, size, pos, bg):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_file).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.topleft= (pos[0] + bg.x, pos[1])
		self.pos = self.rect.topleft
		self.size = size
		self.resize()
	def resize(self):
		self.image = pygame.transform.scale(self.image, self.size)
	
	def update(self):
		self.rect.topleft= (self.pos[0] + game.bg.x, self.pos[1])

class changeable(pygame.sprite.Sprite):
	global game
	def __init__(self, image_file, size, pos, bg):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_file).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.topleft= (pos[0] + bg.x, pos[1])
		self.pos = self.rect.topleft
		self.size = size
		self.resize()
	def resize(self):
		self.image = pygame.transform.scale(self.image, self.size)
	
	def update(self):
		self.rect.topleft= (self.pos[0] + game.bg.x, self.pos[1])


class environment(pygame.sprite.Sprite):
	global game
	def __init__(self, image_file, size, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_file).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.topleft= pos
		self.size = size
		self.resize()
	def resize(self):
		self.image = pygame.transform.scale(self.image, self.size)
		#w = self.size[0]
		#h = self.size[1]
		#if w > h:
			#ratio = w / float(self.metric)
			#new_h = int(h / ratio)
			#self.image = pygame.transform.scale(self.image, (self.metric, new_h))
		#else:
			#ratio = h / float(self.metric)
			#new_w = int(w / ratio)
			#self.image = pygame.transform.scale(self.image, (new_w, self.metric))




pygame.init()
#pygame.font.init()
font = pygame.font.Font("babybody.ttf", 15)
font_1 = pygame.font.Font("babybody.ttf", 32)
#font = pygame.font.SysFont("helvetica", 15)
#font_1 = pygame.font.SysFont("helvetica", 32)
window_size = (800, 600)
timer = pygame.time.Clock()
screen = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption("Lucifer")
FPS = 25

class menu_button(pygame.sprite.Sprite):
	global game
	def __init__(self, topleft, bottomright, action):
		pygame.sprite.Sprite.__init__(self)
		self.x1 = topleft[0]
		self.y1 = topleft[1]
		self.x2 = bottomright[0]
		self.y2 = bottomright[1]
		self.action = action
		self.showflag_1 = 0
		self.showflag_2 = 0
		self.showflag_3 = 0
		self.showflag_4 = 0
		
	def update(self):
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if mouse_x > self.x1 and mouse_x < self.x2 and mouse_y > self.y1 and mouse_y < self.y2:
			if pygame.mouse.get_pressed() == (1, 0, 0):
				if self.action == "quit":
					exit()
				elif self.action == "back":
					game.layer = "menu"
				elif self.action == "show_final_1":
					self.showflag_1 = 1
				elif self.action == "show_final_2":
					self.showflag_2 = 1
				elif self.action == "show_final_3":
					self.showflag_3 = 1
				elif self.action == "show_final_4":
					self.showflag_4 = 1
				else:
					game.layer = self.action




class menu():
	global game
	def __init__(self):
		self.main = pygame.image.load("menu.png").convert_alpha()
		self.about = pygame.image.load("about.png").convert_alpha()
	
		self.buttons = pygame.sprite.Group()
		self.buttons.add(menu_button((520, 313), (670, 360), "play"))
		self.buttons.add(menu_button((520, 374), (670, 420), "about"))
		self.buttons.add(menu_button((520, 434), (670, 475), "quit"))
		self.buttons.add(menu_button((309, 480), (496, 525), "back"))
		self.buttons.add(menu_button((525, 266), (550, 297), "show_final_1"))
		self.buttons.add(menu_button((564, 266), (590, 297), "show_final_2"))
		self.buttons.add(menu_button((600, 266), (627, 297), "show_final_3"))
		self.buttons.add(menu_button((637, 266), (666, 297), "show_final_4"))
	
	def update(self):
		self.buttons.update()
		if game.layer == "menu":
			self.image = self.main
		if game.layer == "about":
			self.image = self.about
		game.screen.blit(self.image, (0, 0))

class game_state:
	# a class used to manage the variables that will be used to program.
	# can save many lines of code whiling passing parameters
	global screen
	def __init__(self):
		self.layer = "menu"
		self.screen = screen
		self.objects = pygame.sprite.Group()
		self.key_set = set()
		self.bullets = []
		self.mymaps = []
		self.bg = background()
		self.mymaps.append(Mymap(self.bg))
		self.Lucifer = lucifer(self.bg, self.mymaps)
		self.M1 = Monster_1(self.mymaps, self.bg, 700, 1)
		self.objects.add(self.M1)
		self.D1 = (Dragon(self.mymaps, self.bg, 2500, 10))
		self.objects.add(self.Lucifer)
		self.environment_objects = pygame.sprite.Group()
		self.environment_objects.add(environment("sun.png", (150, 150), (50, 20)))
		self.environment_objects.add(environment("slogan.png", (600, 80), (100, 520)))
		self.hints = pygame.sprite.Group()
		self.hints.add(hint("hints_1.png", (300, 200), (300, 150), self.bg))
		self.VIM = Boss1(self.mymaps, self.bg, 4000, 100)
		self.objects.add(self.VIM)
		self.main_menu = menu()
		self.changeable_objects = pygame.sprite.Group()
		self.door_closed = changeable("door_closed.png", (20, 230), (4500 + 150 - 20, 170), self.bg)
		self.door_opened = changeable("door_opened.png", (120, 230), (4500 + 150 - 20, 170), self.bg)
		self.changeable_objects.add(self.door_closed)
		self.box_closed = changeable("box_closed.png", (150, 88), (5000 + 150, 400 - 88), self.bg)
		self.box_opened = changeable("box_opened.png", (175, 88), (5000 + 150, 400 - 88), self.bg)
		self.changeable_objects.add(self.box_closed)
		self.digital_rain = rain()
		print len(self.digital_rain.rain)

	def initialization(self):
		self.objects = pygame.sprite.Group()
		self.bullets = []
		self.bg = background()
		self.Lucifer = lucifer(self.bg, self.mymaps)
		self.M1 = Monster_1(self.mymaps, self.bg, 700, 1)
		self.objects.add(self.M1)
		self.D1 = (Dragon(self.mymaps, self.bg, 2500, 10))
		self.objects.add(self.Lucifer)
		self.VIM = Boss1(self.mymaps, self.bg, 4000, 100)
		self.objects.add(self.VIM)


game = game_state()

def show_drop(drop):
	for i in xrange(0, drop.length):
		game.screen.blit(font.render(str(drop.rain_drop[i]), True, drop.rain_color[i]), (drop.pos_x, drop.pos_y - drop.speed * i - drop.delay))
	if drop.pos_y - drop.speed * i - drop.delay > 600 and i == drop.length - 1:
		drop.flag = 1
	drop.pos_y += 10

def show_rain():
	print game.digital_rain.rain[0].pos_y
	for drop in game.digital_rain.rain:
		show_drop(drop)


def show():
	game.screen.fill((0xff, 0xff, 0xff))
	game.screen.blit(game.bg.image, (game.bg.x, game.bg.y))
	#screen.blit(Lucifer.current_image, Lucifer.getloc())
	pygame.draw.rect(game.screen, (100, 100, 150), ((650, 20), game.Lucifer.bling_cooldown_grid), 0)
	pygame.draw.rect(game.screen, (200, 100, 150), ((652, 22), game.Lucifer.bling_cooldown_bar), 0)
	pygame.draw.rect(game.screen, (100, 100, 150), ((200, 20), game.Lucifer.hp_grid), 0)
	pygame.draw.rect(game.screen, (0, 200, 150), ((202, 22), game.Lucifer.hp_grid_bar), 0)
	for b in game.bullets:
		b.update()
		if b.x < 0 or b.x > 800:
			game.bullets.remove(b)
			b.__del__()
		game.screen.blit(b.image, (b.x, b.y))
	game.D1.update()
	if game.D1.dead == 0:
		game.screen.blit(game.D1.image, game.D1.get_loc())
	game.VIM.update()
	if game.Lucifer.pos > 5500:
		game.screen.fill((0, 0, 0))
		show_rain()
		num = int(game.Lucifer.pos - 5500 - game.Lucifer.y + 1)
		game.screen.blit(font_1.render(str(num), True, (100, 200, 100)), (650, 50))
		if num == 42 and K_l in game.key_set:
			exit()

	game.objects.draw(game.screen)
	game.VIM.stars.draw(game.screen)
	game.environment_objects.draw(game.screen)
	game.changeable_objects.draw(game.screen)
	game.VIM.dialog()
	if game.Lucifer.showflag == 1:
		game.screen.blit(game.Lucifer.level_1_final, (100, 30))
		if pygame.mouse.get_pressed() == (1, 0, 0):
			game.Lucifer.showflag = 0
			game.Lucifer.haskey_1 = 0
			game.Lucifer.level_1 = 1
	#print Lucifer.hp

	if game.Lucifer.hp <= 0:
		gameover_img = pygame.image.load("gameover.png").convert_alpha()
		game.screen.blit(gameover_img, (0, 0))

def act():
	if game.layer == "menu":
		game.main_menu.update()
		for b in game.main_menu.buttons:
			if b.showflag_1 == 1:
				print "Asdasdasd"
				game.screen.blit(game.Lucifer.level_1_final, (100, 30))
				if pygame.mouse.get_pressed() == (0, 0, 1):
					b.showflag_1 = 0
			if b.showflag_2 == 1:
				print "Asdasdasd"
				game.screen.blit(game.Lucifer.level_2_final, (100, 30))
				if pygame.mouse.get_pressed() == (0, 0, 1):
					b.showflag_2 = 0
			if b.showflag_3 == 1:
				print "Asdasdasd"
				game.screen.blit(game.Lucifer.level_3_final, (100, 30))
				if pygame.mouse.get_pressed() == (0, 0, 1):
					b.showflag_3 = 0
			if b.showflag_4 == 1:
				print "Asdasdasd"
				game.screen.blit(game.Lucifer.level_4_final, (100, 30))
				if pygame.mouse.get_pressed() == (0, 0, 1):
					b.showflag_4 = 0
	elif game.layer == "about":
		game.main_menu.update()
	elif game.layer == "play":

		if K_r in game.key_set:
			game.initialization()
		if K_ESCAPE in game.key_set:
			game.layer = "menu"
		game.Lucifer.update()
		#for m in monster1s:
			#if m.dead == 1:
				#monster1s.remove(m)
			#m.update(bullets)
		if game.M1.dead == 1:
			game.objects.remove(game.M1)
		game.M1.update()
		game.changeable_objects.update()
		game.digital_rain.update()
		show()

#------- gift version

#img = pygame.image.load("special.png").convert_alpha()
#for i in range(0, 100):
	#screen.blit(img, (0, 0))
	#pygame.display.update()


while True:
	for event in pygame.event.get():
		if event.type is QUIT:
			exit()
		if event.type == KEYDOWN:
			game.key_set.add(event.key)
		if event.type == KEYUP:
			game.key_set.remove(event.key)
	#print Lucifer.y
	#print pygame.mouse.get_pos()[0] - game.bg.x, pygame.mouse.get_pos()[1] -game.bg.y
	print pygame.mouse.get_pos()
	act()
	timer.tick(FPS)
	pygame.display.update()

