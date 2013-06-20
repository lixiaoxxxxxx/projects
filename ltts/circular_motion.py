import math

def d2a(d):
	return (math.pi / 180) * d

def vec(loc1, loc2):
	x1, y1 = loc1
	x2, y2 = loc2
	return (x2 - x1, y2 - y1)

def get_loc(loc, loc1, degree):
	xp = loc1[0]
	yp = loc1[1]
	xr = loc[0]
	yr = loc[1]
	angle = (math.pi / 180) * degree
	xd = (xp - xr) * math.cos(angle) - (yp - yr) * math.sin(angle) + xr
	yd = (xp - xr) * math.sin(angle) + (yp - yr) * math.cos(angle) + yr
	return (xd, yd)

#lp = (2, 0)
#lr = (1, 0)
#d = 45

#print get_loc(lr, lp, d)

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
