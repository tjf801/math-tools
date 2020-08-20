class UnitPrefix:
	# TODO: make this have a name like tera- in front of it or sm idfk
	y = 0.000000000000000000000001
	z = 0.000000000000000000001
	a = 0.000000000000000001
	f = 0.000000000000001
	p = 0.000000000001
	n = 0.000000001
	u = 0.000001
	m = 0.001
	c = 0.01
	da = 0.1
	U = 1.
	d = 10.
	h = 100.
	k = 1000.
	M = 1000000.
	G = 1000000000.
	T = 1000000000000.
	P = 1000000000000000.
	E = 1000000000000000000.
	Z = 1000000000000000000000.
	Y = 1000000000000000000000000.

class Unit:
	def __init__(self, value:float, prefix:UnitPrefix=UnitPrefix.U, **units):
		self.value = value
		self.prefix = prefix
		self.units = units
	
	def __mul__(self, other):
		pass