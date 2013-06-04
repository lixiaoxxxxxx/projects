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
no_mat = (0.0, 0.0, 0.0, 1.0)
mat_ambient = ( 0.7, 0.7, 0.7, 1.0)
mat_ambient_color = ( 0.8, 0.8, 0.2, 1.0)
mat_diffuse = ( 0.1, 0.5, 0.8, 1.0 )
mat_specular = ( 1.0, 1.0, 1.0, 1.0 )
no_shininess = (0, 0, 0, 0)
low_shininess = (5.0, 5, 5,5)
high_shininess = (100.0, 100, 100, 100)
mat_emission = (0.3, 0.2, 0.2, 0.0)

key_mapping = {
		"u" : "u",
		"U" : "U",
		"d" : "d",
		"D" : "D",
		"f" : 1,
		"F" : -1,
		"r" : 2,
		"R" : -2,
		"b" : 3,
		"B" : -3,
		"l" : 4,
		"L" : -4
		}



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
			#print x, "->", x1
			return x1
		if x2 - x < 10e-16:
			#print x, "->", x2
			return x2
		return x
	if x < 0:
		x1 = int(x)
		x2 = x1 - 1
		if x1 - x < 10e-16:
			#print x, "->", x1
			return x1
		if x - x2 < 10e-16:
			#print x, "->", x2
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
	
	def set_state(self, action, f):
		self.xd = 0
		self.yd = 0
		self.zd = 0
		if action == "u":
			temp = self.color["f"]
			if f == 1:
				self.color["f"] = self.color["l"]
				self.color["l"] = self.color["b"]
				self.color["b"] = self.color["r"]
				self.color["r"] = temp
			if f == -1:
				self.color["f"] = self.color["r"]
				self.color["r"] = self.color["b"]
				self.color["b"] = self.color["l"]
				self.color["l"] = temp

			self.x, self.z = get_loc(self.loc[0], self.loc[2], f * -90)

		if action == "f":
			temp = self.color["u"]
			if f == 1:
				self.color["u"] = self.color["r"]
				self.color["r"] = self.color["d"]
				self.color["d"] = self.color["l"]
				self.color["l"] = temp
			if f == -1:
				self.color["u"] = self.color["l"]
				self.color["l"] = self.color["d"]
				self.color["d"] = self.color["r"]
				self.color["r"] = temp
			self.x, self.y = get_loc(self.loc[0], self.loc[1], f * 90)

		if action == "r":
			temp = self.color["u"]
			if f == 1:
				self.color["u"] = self.color["b"]
				self.color["b"] = self.color["d"]
				self.color["d"] = self.color["f"]
				self.color["f"] = temp
			if f == -1:
				self.color["u"] = self.color["f"]
				self.color["f"] = self.color["d"]
				self.color["d"] = self.color["b"]
				self.color["b"] = temp
			self.y, self.z = get_loc(self.loc[1], self.loc[2], f * 90)
		self.x = get_int(self.x)
		self.y = get_int(self.y)
		self.z = get_int(self.z)
		self.loc = [self.x, self.y, self.z]

	def turn_r(self, degree, f):
		self.xd = (f * degree + self.xd) % 360
		loc = get_loc(self.y, self.z, f * degree)
		self.y = loc[0]
		self.z = loc[1]
		if self.xd % 90 == 0:
			self.set_state("r", f)

	def turn_u(self, degree, f):
		self.yd = (f * degree + self.yd) % 360
		loc = get_loc(self.x, self.z, f * -degree)
		self.x = loc[0]
		self.z = loc[1]
		if self.yd % 90 == 0:
			self.set_state("u", f)

	def turn_f(self, degree, f):
		self.zd = (f * degree + self.zd) % 360
		loc = get_loc(self.x, self.y, f * degree)
		self.x = loc[0]
		self.y = loc[1]
		if self.zd % 90 == 0:
			self.set_state("f", f)

		#print self.y
	
	def draw(self):
		glPushMatrix()

		glTranslatef(self.x, self.y, self.z)
		glRotatef(self.xd, 1, 0, 0)
		glRotatef(self.zd, 0, 0, 1)
		glRotatef(self.yd, 0, 1, 0)

		#glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient_color)
		#glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
		#glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
		#)glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess)
		#glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)


		glLineWidth(3.5)
		glColor3f(0.0, 0.0, 0.0)
		glutWireCube (1.)

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
		self.keys = []
		self.cd = 45
		self.blocks = []
		for i in xrange(-1, 2):
			for k in xrange(-1, 2):
				for j in xrange(-1, 2):
					t = Block((j, -k, -i), 0, 0, 0)
					self.blocks.append(t)
		self.f = []
		self.r = []
		self.b = []
		self.l = []
	
	def redefine(self, flag):
		del self.f[:]
		del self.r[:]
		del self.b[:]
		del self.l[:]
		if flag == "r":
			for b in self.blocks:
				if b.z == 1:
					self.f.append(b)
				if b.x == 1:
					self.r.append(b)
				if b.z == -1:
					self.b.append(b)
				if b.x == -1:
					self.l.append(b)

		if flag == "g":
			for b in self.blocks:
				if b.x == 1:
					self.f.append(b)
				if b.z == -1:
					self.r.append(b)
				if b.x == -1:
					self.b.append(b)
				if b.z == 1:
					self.l.append(b)

		if flag == "m":
			for b in self.blocks:
				if b.z == -1:
					self.f.append(b)
				if b.x == -1:
					self.r.append(b)
				if b.z == 1:
					self.b.append(b)
				if b.x == 1:
					self.l.append(b)
			
		if flag == "b":
			for b in self.blocks:
				if b.x == -1:
					self.f.append(b)
				if b.z == 1:
					self.r.append(b)
				if b.x == 1:
					self.b.append(b)
				if b.z == -1:
					self.l.append(b)


	
	def turn_u(self, f):
		for b in self.blocks:
			if b.y == 1:
				b.turn_u(2, f)
		glutPostRedisplay()

	def turn_d(self, f):
		for b in self.blocks:
			if b.y == -1:
				b.turn_u(2, f)
		glutPostRedisplay()

	def turn_f(self, f):
		for b in self.blocks:
			if b.z == 1:
				b.turn_f(2, f)
		glutPostRedisplay()

	def turn_b(self, f):
		for b in self.blocks:
			if b.z == -1:
				b.turn_f(2, f)
		glutPostRedisplay()

	def turn_r(self, f):
		for b in self.blocks:
			if b.x == 1:
				b.turn_r(2, f)
		glutPostRedisplay()
	
	def turn_l(self, f):
		for b in self.blocks:
			if b.x == -1:
				b.turn_r(2, f)
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
	global vp
	glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(vp.x1, vp.y1, vp.z1, vp.x2, vp.y2, vp.z2, 0.0, 1.0, 0.0)

	cube.draw()

	glutSwapBuffers()


def printFunction( name ):
	def onevent( *args ):
		print '%s -> %s'%(name, ", ".join( [str(a) for a in args ]))
	return onevent

def action(key):
	if key == 'u':
		cube.turn_u(-1)
	if key == 'U':
		cube.turn_u(1)
	if key == 'd':
		cube.turn_d(1)
	if key == 'D':
		cube.turn_d(-1)
	if key == 1 or key == 5:
		cube.turn_f(-1)
	if key == -1 or key == -5:
		cube.turn_f(1)
	if key == 2 or key == 6:
		cube.turn_r(-1)
	if key == -2 or key == -6:
		cube.turn_r(1)
	if key == 3 or key == 7:
		cube.turn_b(1)
	if key == -3 or key == -7:
		cube.turn_b(-1)
	if key == 4:
		cube.turn_l(1)
	if key == -4:
		cube.turn_l(-1)

def key_redefine(k, f):
	if type(k) == str:
		return k
	if k > 0:
		return k + f
	else:
		return k - f

def keyboardfunc(key, x, y):
	#print cube.keys
	if key == 'q':
		exit()
	else:
		cube.keys.append(key)

def ontimer(x):
	global vp
	#print cube.cd, cube.keys
	if cube.cd and len(cube.keys):
		cube.cd -= 1
		action(key_redefine(key_mapping[cube.keys[0]], vp.f))
	else:
		cube.cd = 45
		if len(cube.keys):
			del cube.keys[0]
	glutTimerFunc(20, ontimer, 1)

#mouse_before = (0, 0)
#mouse_after = (0, 0)

#def mouse(button, state, x, y):
	#global mouse_before
	##global mouse_after
	#if state == 0:
		#print x, y
		#mouse_before = (x, y)
	#if state == 1:
		#print x, y
		#mouse_after = (x, y)
		#print mouse_before

class View_point:
	global cube
	def __init__(self):
		self.x1 = 3
		self.y1 = 3
		self.z1 = 3
		self.x2 = -1
		self.y2 = -1
		self.z2 = -1
		self.dis = self.x1 ** 2 + self.y1 ** 2 + self.z1 ** 2
		self.d = self.dis ** 0.5
		self.f = 0
	
	def turn_x(self, flag):
		global cube
		if flag > 0:
			a = 1
		else:
			a = -1
		self.x1, self.z1 = get_loc(self.x1, self.z1, a * 3)
		self.x2, self.z2 = get_loc(self.x2, self.z2, a * 3)
		d = get_degree((0, 0), (self.x1, self.z1))
		#print d
		if cube.cd == 45:
			if d > 45 and d <= 135:
				#cube.redefine("r")
				print "front is red"
				self.f = 0
			if d <= 45 or d > 315:
				#cube.redefine("g")
				print "front is green"
				self.f = 1
			if d > 225 and d <= 315:
				#cube.redefine("m")
				print "front is magenta"
				self.f = 2
			if d > 135 and d <= 225:
				#cube.redefine("b")
				print "front is blue"
				self.f = 3
			

		display()
	
	def turn_y(self, flag):
		if flag > 0:
			a = 1
		else:
			a = -1
		self.y1 += a * 0.15
		if self.y1 <= -self.d:
			self.y1 = -self.d 
		elif self.y1 >= self.d:
			self.y1 = self.d
		else:
			x = ((self.dis - self.y1 ** 2) / (self.x1 ** 2 + self.z1 ** 2)) ** 0.5
			self.x1 *= x
			self.z1 *= x
			self.x2 *= x
			self.z2 *= x
		self.y2 = (-1./3) * self.y1
		display()

vp = View_point()

lx = 0
ly = 0
def motion(x, y):
	global lx, ly
	global vp
	if lx == 0 and ly == 0:
		lx = x
		ly = y
	if abs(x - lx) >= 1 or abs(y - ly) >= 1:
		vp.turn_x(x - lx)
		vp.turn_y(y - ly)
		lx = x
		ly = y


if __name__ == "__main__":
	newArgv = glutInit(sys.argv)
	print 'newArguments', newArgv
	glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(600, 600)
	glutInitWindowPosition(100, 100)
	window = glutCreateWindow("hello")


	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LESS)

	#light_position = (5, 5, 5, 0)
	#glLightfv(GL_LIGHT0, GL_POSITION, light_position)
	#glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
	#glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
	#glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (-1, -1, -1, 0))
	#glEnable(GL_LIGHTING)
	#glEnable(GL_LIGHT0)
	#glEnable(GL_COLOR_MATERIAL)

	print "set done"
	glutKeyboardFunc(keyboardfunc)
	print 'window', repr(window)
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutTimerFunc(20, ontimer, 1)
	#glutMouseFunc(mouse)
	glutMotionFunc(motion)
	#glutEntryFunc(printFunction( 'Entry' ))
	#glutKeyboardFunc( printFunction( 'Keyboard' ))
	#glutKeyboardUpFunc( printFunction( 'KeyboardUp' ))
	#glutPassiveMotionFunc( printFunction( 'PassiveMotion' ))
	#glutVisibilityFunc( printFunction( 'Visibility' ))
	#glutWindowStatusFunc( printFunction( 'WindowStatus' ))
	#glutSpecialFunc( printFunction( 'Special' ))
	#glutSpecialUpFunc( printFunction( 'SpecialUp' ))

	#glutIdleFunc( idle )
	glutMainLoop()
