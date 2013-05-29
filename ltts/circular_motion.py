import math

def get_degree(loc1, loc2, dis):
	y = loc2[1] - loc1[1]
	x = loc2[0] - loc1[0]
	degree = math.degrees(math.asin(abs(y) / dis))
	if x < 0 and y > 0:
		degree += 90
	elif x < 0 and y < 0:
		degree += 180
	elif x > 0 and y < 0:
		degree += 270
	return degree

def cal_loc(sun, p):
	p.degree += p.direction * p.speed
	y = p.dis * math.sin((math.pi / 180) * p.degree)
	x = p.dis * math.cos((math.pi / 180) * p.degree)
	new_x = p.loc[0] + x
	new_y = p.loc[1] + y
	new_loc = (new_x, new_y)

	return new_loc



loc1 = (0., 0.)
loc2 = (-1., -1.)
dis = 2 ** 0.5
print dis
print get_degree(loc1, loc2, dis)
cal_loc((0, 0), 2, 1, 0, 45)
