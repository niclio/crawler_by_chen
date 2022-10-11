import math

def cmul(c, a):
	r = a.copy()
	for i in range(len(a)):
		r[i] = c*r[i]
	return r

def neg(a):
	return cmul(-1.0, a)

def add(a,b):
	r = [0]*len(a)
	for i in range(len(a)):
		r[i] = a[i]+b[i]
	return r

def sub(a,b):
	return add(a, neg(b))

def dot(a,b):
	r = 0.0
	for i in range(len(a)):
		r += a[i]*b[i]
	return r

def length(a):
	r = 0.0
	for x in a:
		r += x**2
	return math.sqrt(r)

def distance(a,b):
	return length(sub(a,b))

