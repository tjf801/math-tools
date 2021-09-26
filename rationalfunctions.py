import polynomials

class RationalFunction:
	def __init__(self, numerator: polynomials.Polynomial, denominator: polynomials.Polynomial):
		gcd = polynomials.PolynomialGCD(numerator, denominator)
		self.holes = gcd.solve() if gcd!=1 else ()
		self.numerator = numerator//gcd if gcd != 1 else numerator
		self.denominator = denominator//gcd if gcd != 1 else denominator
	
	def __str__(self):
		return f"({self.numerator*polynomials.polynomial_from_roots(self.holes)})/({self.denominator*polynomials.polynomial_from_roots(self.holes)})"
	
	def __mul__(self, other):
		if isinstance(other, RationalFunction):
			return RationalFunction(self.numerator*other.numerator, self.denominator*other.denominator)
	
	def __neg__(self):
		return RationalFunction(-self.numerator, self.denominator)
	
	def __add__(self, other):
		if isinstance(other, RationalFunction):
			return RationalFunction(self.numerator*other.denominator+self.denominator*other.numerator, self.denominator*other.denominator)
	
	def __sub__(self, other):
		if isinstance(other, RationalFunction):
			return self+(-other)
	
	@property
	def reciprocal(self):
		return RationalFunction(self.denominator, self.numerator)
	
	def __div__(self, other):
		if isinstance(other, RationalFunction):
			return RationalFunction(self.numerator*other.denominator, self.denominator*other.numerator)
	
	def __call__(self, value):
		if value in self.holes: raise ValueError("value is at a hole")
		return self.numerator(value)/self.denominator(value)
	
	def vertical_asymptotes(self):
		return self.denominator.solve()
	
	def horizontal_asymptote(self):
		return self.numerator//self.denominator
	
	def zeros(self):
		return self.numerator.solve()

if __name__=="__main__":
	from polynomials import Polynomial as P
	
	f = RationalFunction(P(2, 0, 0, 0), P(1, 1, -12))
	
	print(f"f(x)={f}")
	print("holes:", f.holes)
	print("horizontal:", f.horizontal_asymptote())
	print("vertical:", f.vertical_asymptotes())
	#print("zeros:", f.zeros())
	print("y-int:", f(0))