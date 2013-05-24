import pygame
import sys
from pygame.locals import *
from random import randint

SIZE_X , SIZE_Y, BN = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

print SIZE_X, SIZE_Y, BN

cp = max(SIZE_X, SIZE_Y)
r= int(float(500) / int(cp))

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((r * SIZE_X + r / 10, r * SIZE_Y 
	+ r / 10), 0, 32)

bomb_img = 'shit.png'
flag_img = 'flag.png'
BOMB = pygame.image.load(bomb_img).convert_alpha()
FLAG = pygame.image.load(flag_img).convert_alpha()

FLAG = pygame.transform.scale(FLAG, (r, r))
BOMB = pygame.transform.scale(BOMB, (
	int(float(r) * 0.8), int(float(r) * 0.8)))

screen.fill((0xff, 0xff, 0xff))
pygame.display.set_caption("mine")
font = pygame.font.Font("babybody.ttf", int(30 * (float(r) / 50)))
timer = pygame.time.Clock()

offset = int(5 * float(r) / 50)

FPS = 10

class Selection:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.color = (180, 0, 0)
		self.rect = ((self.x * r, self.y * r), (r + offset, r + offset))

	def move_left(self):
		self.x = max(0, self.x - 1)
		self.rect = ((self.x * r, self.y * r), (r + offset, r + offset))

	def move_right(self):
		self.x = min(SIZE_X - 1, self.x + 1)
		self.rect = ((self.x * r, self.y * r), (r + offset, r + offset))

	def move_up(self):
		self.y = max(0, self.y - 1)
		self.rect = ((self.x * r, self.y * r), (r + offset, r + offset))

	def move_down(self):
		self.y = min(SIZE_Y - 1, self.y + 1)
		self.rect = ((self.x * r, self.y * r), (r + offset, r + offset))

class Grid:
	def __init__(self, size_x, size_y, bn):
		self.x = size_x
		self.y = size_y
		self.grid = []
		self.num_grid = []
		self.flags = []
		self.grid_init(size_x, size_y)
		self.bn = bn
		self.set_bomb(self.bn)
	
	def grid_init(self, x, y):
		for i in xrange(0, x):
			temp = []
			t = []
			f = []
			for j in xrange(0, y):
				temp.append(0)
				t.append(0)
				f.append(0)
			self.grid.append(temp)
			self.num_grid.append(t)
			self.flags.append(f)
	
	def set_flag(self, x, y, f):
		if f is K_a:
			self.flags[x][y] = 1
			if self.num_grid[x][y] == 0:
				self.BFS(x, y)
		if f is K_d:
			if self.flags[x][y] == 2:
				self.flags[x][y] = 0
			elif self.flags[x][y] == 0:
				self.flags[x][y] = 2
		if f is K_s:
			count = 0
			for i in xrange(x - 1, x + 2):
				for j in xrange(y - 1, y + 2):
					if self.valid(i, j):
						if self.flags[i][j] == 2:
							count += 1
			
			if count >= self.num_grid[x][y]:
				for i in xrange(x - 1, x + 2):
					for j in xrange(y - 1, y + 2):
						if self.valid(i, j):
							if self.flags[i][j] != 2:
								self.flags[i][j] = 1
							if self.num_grid[i][j] == 0:
								self.BFS(i, j)

	
	def valid(self, x, y):
		if x >= 0 and x < self.x and y >= 0 and y < self.y:
			return True
		else:
			return False

	def add_bomb(self, x, y):
		self.grid[x][y] = 1
		for i in xrange (x - 1, x + 2):
			for j in xrange(y - 1, y + 2):
				if self.valid(i, j):
					self.num_grid[i][j] += 1
	
	def set_bomb(self, bn):
		for i in xrange(0, self.x):
			for j in xrange(0, self.y):
				x = randint(0, self.x * self.y)
				if x <= bn:
					self.add_bomb(i, j)
	
	def get_nb(self, x, y):
		temp = []
		for i in xrange(x - 1, x + 2):
			for j in xrange(y - 1, y + 2):
				if self.valid(i, j):
					if self.num_grid[i][j] == 0:
						temp.append((i, j))
					self.flags[i][j] = 1

		return temp
	
	def BFS(self, x, y):
		unvisited = []
		unvisited.append((x, y))
		now = 0
		while now != len(unvisited):
			t_x, t_y = unvisited[now]
			temp = self.get_nb(t_x, t_y)
			unvisited = unvisited + [x for x in temp if x not in unvisited]
			now += 1

class Game:

	def __init__(self, x, y, bn):
		self.grid = Grid(x, y, bn)
		self.key_set = set()
		self.selection = Selection()
	
	def __del__(self):
		pass

	
	def control(self, event):
		if event.type == KEYDOWN:
			self.key_set.add(event.key)
			self.grid.set_flag(self.selection.x, self.selection.y, event.key)
		if event.type == KEYUP:
			self.key_set.remove(event.key)


	def update(self):
		if K_h in self.key_set:
			self.selection.move_left()
		if K_l in self.key_set:
			self.selection.move_right()
		if K_j in self.key_set:
			self.selection.move_down()
		if K_k in self.key_set:
			self.selection.move_up()


game = Game(SIZE_X, SIZE_Y, BN)

def restart():
	global game
	game = Game(SIZE_X, SIZE_Y, BN)

def display():
	screen.fill((0xff, 0xff, 0xff))
	pygame.draw.rect(screen, game.selection.color, game.selection.rect, 5)

	offset = int(5 * float(r) / 50)

	for x in xrange(0, SIZE_X):
		for y in xrange(0, SIZE_Y):
			if game.grid.num_grid[x][y] != 0:
				screen.blit(font.render(str(game.grid.num_grid[x][y]),
					True, (100, 100, 100, 0xff)), ((x * r + offset), y * r + offset))
			if game.grid.grid[x][y] == 1:
				screen.blit(BOMB, (x * r + offset, y * r + offset))
			if game.grid.flags[x][y] != 1: 
				pygame.draw.rect(screen, (0, 0, 200), ((x * r + offset,
					y * r + offset), (r - offset, r - offset)), 0)
			if game.grid.flags[x][y] == 2:
				screen.blit(FLAG, (x * r + offset, y * r + offset))

	pygame.display.update()


while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN:
			if event.key == K_r:
				restart()
			if event.key == K_q:
				exit()
		game.control(event)
	
	game.update()
	display()
	timer.tick(FPS)
