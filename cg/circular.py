import math

def get_rad(degree):
	return (math.pi / 180) * degree

def get_loc(x, y, degree):
	angle = get_rad(degree)
	x1 = math.cos(angle) * x - math.sin(angle) * y
	y1 = math.cos(angle) * y + math.sin(angle) * x
	print x1, y1
	print x1 ** 2 + y1 ** 2

get_loc(0, 1, 30)

