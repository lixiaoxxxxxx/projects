import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import time

cl_white = (1.0,1.0,1.0)
cl_magenta = (1.0,0.0,1.0)
cl_black=(0.0,0.0,0.0)
cl_red=(1.0,0.0,0.0)
cl_green=(0.0,1.0,0.0)
cl_blue=(0.0,0.0,1.0)
cl_yellow=(1.0,1.0,0.0)
cl_purple=(1.0,0.0,1.0)


def get_loc(x, y, degree):
	angle = (math.pi / 180) * degree
	x1 = math.cos(angle) * x - math.sin(angle) * y
	y1 = math.cos(angle) * y + math.sin(angle) * x
	return x1, y1

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


def get_int(x):
	if x > 0:
		x1 = int(x)
		x2 = x1 + 1
		if x - x1 < 10e-16:
			print x, "->", x1
			return x1
		if x2 - x < 10e-16:
			print x, "->", x2
			return x2
		return x
	if x < 0:
		x1 = int(x)
		x2 = x1 - 1
		if x1 - x < 10e-16:
			print x, "->", x1
			return x1
		if x - x2 < 10e-16:
			print x, "->", x2
			return x2
	return x


class Block:
	def __init__(self, center, xd, yd, zd):
		self.x, self.y, self.z = center
		self.xd = xd
		self.yd = yd 
		self.zd = zd
		self.loc = [self.x, self.y, self.z]
		self.color = {
				"f" : cl_red,
				"b" : cl_magenta,
				"u" : cl_yellow,
				"d" : cl_white,
				"l" : cl_blue,
				"r" : cl_green}
	
	def set_state(self, action):
		self.xd = 0
		self.yd = 0
		self.zd = 0
		if action == "u":
			temp = self.color["f"]
			self.color["f"] = self.color["l"]
			self.color["l"] = self.color["b"]
			self.color["b"] = self.color["r"]
			self.color["r"] = temp
			#self.x, self.z = u_turn[(self.loc[0], self.loc[2])]
			self.x, self.z = get_loc(self.loc[0], self.loc[2], -90)
			self.x = get_int(self.x)
			self.z = get_int(self.z)
			self.loc = [self.x, self.y, self.z]

		if action == "f":
			temp = self.color["u"]
			self.color["u"] = self.color["r"]
			self.color["r"] = self.color["d"]
			self.color["d"] = self.color["l"]
			self.color["l"] = temp
			#self.x, self.y = f_turn[(self.loc[0], self.loc[1])]
			self.x, self.y = get_loc(self.loc[0], self.loc[1], 90)
			self.x = get_int(self.x)
			self.y = get_int(self.y)
			self.loc = [self.x, self.y, self.z]
			print self.loc

		if action == "r":
			temp = self.color["u"]
			self.color["u"] = self.color["b"]
			self.color["b"] = self.color["d"]
			self.color["d"] = self.color["f"]
			self.color["f"] = temp
			#self.x, self.y = f_turn[(self.loc[0], self.loc[1])]
			self.y, self.z = get_loc(self.loc[1], self.loc[2], 90)
			self.y = get_int(self.y)
			self.z = get_int(self.z)
			self.loc = [self.x, self.y, self.z]
			print self.loc

	def turn_r(self, degree):
		self.xd = (degree + self.xd) % 360
		loc = get_loc(self.y, self.z, degree)
		self.y = loc[0]
		self.z = loc[1]
		if self.xd % 90 == 0:
			self.set_state("r")

	def turn_u(self, degree):
		self.yd = (degree + self.yd) % 360
		loc = get_loc(self.x, self.z, -degree)
		self.x = loc[0]
		self.z = loc[1]
		if self.yd % 90 == 0:
			self.set_state("u")
		#print self.yd
		#print self.x

	def turn_f(self, degree):
		self.zd = (degree + self.zd) % 360
		loc = get_loc(self.x, self.y, degree)
		self.x = loc[0]
		self.y = loc[1]
		if self.zd % 90 == 0:
			self.set_state("f")

		#print self.y
	
	def draw(self):
		glPushMatrix()

		glTranslatef(self.x, self.y, self.z)
		glRotatef(self.xd, 1, 0, 0)
		glRotatef(self.zd, 0, 0, 1)
		glRotatef(self.yd, 0, 1, 0)

		glBegin(GL_POLYGON)
		glColor3fv(self.color["f"])
		#glNormal3f(0., 0., 1.)
		glVertex3f(-.5, .5, .5)
		glVertex3f(.5, .5, .5)
		glVertex3f(.5, -.5, .5)
		glVertex3f(-.5, -.5, .5)
		glEnd()

		glBegin(GL_POLYGON)
		glColor3fv(self.color["b"])
		#glNormal3f(0., 0., -1.)
		glVertex3f(-.5, .5, -.5)
		glVertex3f(.5, .5, -.5)
		glVertex3f(.5, -.5, -.5)
		glVertex3f(-.5, -.5, -.5)
		glEnd()

		glBegin(GL_POLYGON)
		glColor3fv(self.color["u"])
		#glNormal3f(0., 1., 0.)
		glVertex3f(-.5, .5, -.5)
		glVertex3f(.5, .5, -.5)
		glVertex3f(.5, .5, .5)
		glVertex3f(-.5, .5, .5)
		glEnd()

		glBegin(GL_POLYGON)
		glColor3fv(self.color["d"])
		#glNormal3f(0., -1., 0.)
		glVertex3f(-.5, -.5, -.5)
		glVertex3f(.5, -.5, -.5)
		glVertex3f(.5, -.5, .5)
		glVertex3f(-.5, -.5, .5)
		glEnd()

		glBegin(GL_POLYGON)
		glColor3fv(self.color["l"])
		#glNormal3f(-1, 0., 0.)
		glVertex3f(-.5, .5, -.5)
		glVertex3f(-.5, -.5, -.5)
		glVertex3f(-.5, -.5, .5)
		glVertex3f(-.5, .5, .5)
		glEnd()

		glBegin(GL_POLYGON)
		glColor3fv(self.color["r"])
		#glNormal3f(1. + x, 0., 0.)
		glVertex3f(.5, .5, -.5)
		glVertex3f(.5, -.5, -.5)
		glVertex3f(.5, -.5, .5)
		glVertex3f(.5, .5, .5)
		glEnd()
		glPopMatrix()

class Cube:
	def __init__(self):
		self.blocks = []
		for i in xrange(-1, 2):
			for k in xrange(-1, 2):
				for j in xrange(-1, 2):
					t = Block((j, -k, -i), 0, 0, 0)
					self.blocks.append(t)

	
	def turn_u(self):
		for b in self.blocks:
			if b.y == 1:
				b.turn_u(10)
		glutPostRedisplay()

	def turn_f(self):
		for b in self.blocks:
			if b.z == 1:
				b.turn_f(10)
		glutPostRedisplay()

	def turn_r(self):
		for b in self.blocks:
			if b.x == 1:
				b.turn_r(10)
		glutPostRedisplay()
	
	def draw(self):
		for b in self.blocks:
			b.draw()
	
	

cube = Cube()

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective (60.0, w / h, .1, 200.0)
	glMatrixMode(GL_MODELVIEW)

def display():
	glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(4.5, 3.5, 3.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0)

	cube.draw()

	glutSwapBuffers()


def printFunction( name ):
	def onevent( *args ):
		print '%s -> %s'%(name, ", ".join( [str(a) for a in args ]))
	return onevent

def keyboardfunc(key, x, y):
	if key == 'q':
		exit()
	
	if key == 'u':
		cube.turn_u()

	if key == 'f':
		cube.turn_f()

	if key == 'r':
		cube.turn_r()

if __name__ == "__main__":
	newArgv = glutInit(sys.argv)
	print 'newArguments', newArgv
	glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(600, 600)
	glutInitWindowPosition(100, 100)
	window = glutCreateWindow("hello")
	glutKeyboardFunc(keyboardfunc)
	glEnable(GL_DEPTH_TEST)
	print 'window', repr(window)
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	#glutMouseFunc(printFunction( 'Mouse' ))
	#glutEntryFunc(printFunction( 'Entry' ))
	#glutKeyboardFunc( printFunction( 'Keyboard' ))
	#glutKeyboardUpFunc( printFunction( 'KeyboardUp' ))
	#glutMotionFunc( printFunction( 'Motion' ))
	#glutPassiveMotionFunc( printFunction( 'PassiveMotion' ))
	#glutVisibilityFunc( printFunction( 'Visibility' ))
	#glutWindowStatusFunc( printFunction( 'WindowStatus' ))
	#glutSpecialFunc( printFunction( 'Special' ))
	#glutSpecialUpFunc( printFunction( 'SpecialUp' ))
	#glutTimerFunc( 1000, ontimer, 23 )

	#glutIdleFunc( idle )
	glutMainLoop()
