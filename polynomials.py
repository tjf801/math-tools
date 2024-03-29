from typing import Union, List, Tuple, Any
import builtins, inspect
import basicfunctions

class __PolynomialMetaClass(type):
	def __getitem__(cls, key: type):
		# called when you do something like Polynomial[float]
		if not inspect.isclass(key): raise TypeError("Parameters to generic types must be types. Got {thing}.".format(thing=key))
		class TypedPolynomial(cls): type = key
		return TypedPolynomial

class Polynomial(metaclass=__PolynomialMetaClass):
	"""
	TODO: finish doc
	coefficient objects must have:
		__repr__ or __str__ NOTE: only repr will get called though, due to no PEP 3140.
		__eq__ for accurate testing using the '==', '!=', 'in', etc. operators
		__neg__ to support the unary '-' operator
		__add__ for polynomial addition, and addition has these properties:
			0 + object == object
			object + (-object) == 0 (or at be similar to zero in that it is the additive identity for the object)
			also must be communative
		__sub__ for polynomial subtraction:
			object - object == 0 (or at be similar to zero in that it is the additive identity for the object)
			0 - object == -object
		__mul__ for polynomial multiplication
			also scalar multiplication for derivative
	"""
	
	type = Any
	
	def __init__(self, *coefficients, type:type=Any):
		self.type = type if type is not Any else self.type
		if len(coefficients)==1 and isinstance(coefficients[0], Polynomial): self.coefficients = coefficients[0].coefficients
		else: self.coefficients = list(coefficients)
		if self.type is not Any:
			for i, coeff in enumerate(self.coefficients):
				try: self.coefficients[i] = self.type(coeff) if coeff != 0 else coeff
				except TypeError: self.type = Any #raise TypeError('coefficient {c} is not of type {type}'.format(c=coeff, type=self.type.__name__))\
			if self.type is not Any:
				try: assert(all(isinstance(c, self.type) or c==0 for c in self.coefficients)) #if this fails, I done fucked up (and its not your fault)
				except AssertionError as ಠ_ಠ: print(self.type, [(c, self.type(c), isinstance(c, self.type)) for c in self.coefficients]); raise ಠ_ಠ
	
	def __str__(self) -> str:
		# ¹²³⁴⁵⁶⁷⁸⁹⁰
		
		get_superscript = lambda x: str(x).replace('0', '⁰').replace('1', '¹').replace('2', '²').replace('3', '³').replace('4', '⁴').replace('5', '⁵').replace('6', '⁶').replace('7', '⁷').replace('8', '⁸').replace('9', '⁹')
		d = self.degree
		
		string = ""
		for i, c in reversed(list(enumerate(reversed(self.coefficients)))):
			string += ((('+' if i!=d else '') if c>=0 else '-') if type(c) in (int, float) else (('+' if i!=d else '') if c!=-1 else '-')) if c not in (0,) else ''
			if c not in (1, 0, -1) or (i==0 and c in (1, -1)) or (d==0): string+= str(abs(c)) if type(c) in (int, float) else (str(c) if string=='' else (str(-c) if string[-1]=='-' else str(c)))
			if i!=0 and c!=0: string+='x'
			if i not in (0, 1) and c!=0: string+=get_superscript(i)
		return string
	
	def __repr__(self) -> str:
		# PEP 3140 should be a thing, why the f**k was it rejected???
		# because it isn't, this returns the repr of all the coefficients, and looks ugly as F**K for non-int/float polynomials
		# HURR DURR Polynomial<TestType>(<__main__.TestType object at 0x0000028C6C68C700>, <__main__.TestType object at 0x0000028C6C68C970>, <__main__.TestType object at 0x0000028C6C68C6A0>)
		# return str(self)
		return f"Polynomial{'<' + self.type.__name__ + '>' if self.type is not Any else ''}{str(tuple(self.coefficients))}"
	
	def __getitem__(self, index: Union[int, slice]):
		if isinstance(index, int):
			if index >= len(self.coefficients): return 0 # return additive identity/multaplicitive absorber for arbitrary class?
			elif index < 0: raise IndexError('polynomial indices must not be negative')
			return self.coefficients[-index-1]
		elif isinstance(index, slice):
			start = index.start if index.start is not None else 0
			stop = index.stop if index.stop is not None else len(self)
			step = index.step if index.step is not None else 1
			if start < 0: raise IndexError('polynomial indices must not be negative')
			if stop < 0: raise IndexError('polynomial indices must not be negative')
			return Polynomial(*reversed([self[i] for i in (range(start, stop, step) if step>0 else range(stop-1, start-1, step))]))
		else: raise TypeError("expected polynomial index to be int or slice, not {type.__name__}".format(type=type(index)))
	
	def __setitem__(self, index: Union[int, slice], value):
		if not self.type is Any and not isinstance(value, self.type) and not (self.type in (float, int) and type(value) in (float, int)): raise TypeError('{T} polynomial coefficients must be {T}, not {type}'.format(T=self.type.__name__, type=type(value).__name__))
		if isinstance(index, int):
			if index >= len(self.coefficients): self.coefficients = [0]*(1+index-len(self.coefficients)) + self.coefficients
			elif index < 0: raise IndexError('polynomial indices must not be negative')
			self.coefficients[-index-1] = value
		elif isinstance(index, slice):
			start = index.start if index.start is not None else 0
			stop = index.stop if index.stop is not None else len(self)
			step = index.step if index.step is not None else 1
			if start < 0: raise IndexError('polynomial indices must not be negative')
			if stop < 0: raise IndexError('polynomial indices must not be negative')
			raise NotImplementedError
		else: raise TypeError("expected polynomial index to be int or slice, not {type.__name__}".format(type=type(index)))
	
	def __delitem__(self, index: Union[int, slice]):
		if isinstance(index, int): del self.coefficients[-index-1]
		elif isinstance(index, slice): raise NotImplementedError
		else: raise TypeError("expected polynomial index to be int or slice, not {type.__name__}".format(type=type(index)))
	
	def get_term(self, index: Union[int, slice]):
		if isinstance(index, int):
			return Polynomial(self[index])<<index
		elif isinstance(index, slice): raise NotImplementedError
		else: raise TypeError("expected polynomial index to be int or slice, not {type.__name__}".format(type=type(index)))
	
	@property
	def degree(self) -> int:
		d = 0
		for i, c in enumerate(self.coefficients):
			if c != 0: d = len(self.coefficients)-i-1; break
		return d
	
	@property
	def leading_coefficent(self):
		return self[self.degree]
	
	def copy(self):
		return Polynomial(*self.coefficients)
	
	def trim_trailing_zeros(self):
		if self.type is float:
			for i, c in enumerate(self):
				if int(c)==c: self[i]=int(c)
		#if self.type is not Any and all(isinstance(c, int) for c in self): self.type = int
		self.coefficients = self.coefficients[-self.degree-1:]
		return self
	
	def cast(self, type:type):
		if type is list: return [*self.coefficients]
		elif type is tuple: return tuple([*self.coefficients])
		if not type is Any:
			try: return Polynomial(*(type(c) for c in self.coefficients))
			except TypeError: raise TypeError("unable to cast {type1.__name__} polynomial to {type2.__name__} polynomial".format(type1=self.type, type2=type))
	
	def __bool__(self) -> bool:
		return not (self.degree == 0 and self[0] == 0)
	
	def __len__(self) -> int:
		return self.degree + 1
	
	def __iter__(self):
		self.iterindex = -1
		return self
	
	def __next__(self):
		self.iterindex += 1
		if self.iterindex>self.degree: del self.iterindex; raise StopIteration
		return self[self.iterindex]
	
	# arithmetic functions
	
	def __eq__(self, other) -> bool:
		if isinstance(other, (list, tuple)): other = Polynomial(*other)
		elif self.degree != 0 and not isinstance(other, Polynomial): return False
		elif not isinstance(other, Polynomial): other = Polynomial(other)
		return all(self[i]==other[i] for i in range(max(len(self), len(other))))
	
	def __ne__(self, other) -> bool:
		# is this slower than not having it?
		# edit: yes it is, by 0.5 microseconds per 10,000 comparisons
		return not self==other
	
	def __pos__(self):
		return self.copy()
	
	def __neg__(self):
		return Polynomial(*reversed([-a for a in self]))
	
	def __lshift__(self, num_places: int):
		if not isinstance(num_places, int): raise TypeError('expected integer value in polynomial left shift')
		if num_places<0: return self>>-num_places
		try: return Polynomial(*(self.coefficients + [self.type(0)]*num_places))
		except TypeError: return Polynomial(*(self.coefficients + [0]*num_places))
	
	def __rshift__(self, num_places: int):
		if not isinstance(num_places, int): raise TypeError('expected integer value in polynomial right shift')
		if num_places==0: return self.copy()
		elif num_places<0: return self<<-num_places
		return Polynomial(*(self.coefficients[:-num_places]))
	
	def __add__(self, other):
		if not isinstance(other, Polynomial): other = Polynomial(other)
		return Polynomial(*reversed([self[i]+other[i] for i in range(max(len(self), len(other)))])).trim_trailing_zeros()
	def __radd__(self, other):
		return self+other
	def __iadd__(self, other):
		if not isinstance(other, Polynomial): other = Polynomial(other)
		for i in range(max(len(self), len(other))): self[i]+=other[i]
		return self.trim_trailing_zeros()
	
	def __sub__(self, other):
		if not isinstance(other, Polynomial): other = Polynomial(other)
		return Polynomial(*reversed([self[i]-other[i] for i in range(max(len(self), len(other)))])).trim_trailing_zeros()
	def __rsub__(self, other):
		return -self+other
	def __isub__(self, other):
		if not isinstance(other, Polynomial): other = Polynomial(other)
		for i in range(max(len(self), len(other))): self[i]-=other[i]
		return self.trim_trailing_zeros()
	
	def __mul__(self, other):
		if not isinstance(other, Polynomial): return Polynomial(*reversed([other * c for c in self])).trim_trailing_zeros() # X * Poly(a, b, c) -> Poly(X*a, X*b, X*c)
		result = Polynomial(type=self.type)
		for i in range(len(self)):
			for j in range(len(other)):
				result[i+j] += self[i] * other[j]
		return result.trim_trailing_zeros()
	def __rmul__(self, other):
		return self*other
	
	def __divmod__(self, other)->tuple:
		if not isinstance(other, Polynomial): other = Polynomial(other)
		
		Q = other.cast(float) if self.type is int else other
		R = self.copy()
		if self.type is int: R = R.cast(float)
		result = Polynomial(type=float if self.type is int else self.type)
		
		for i in range(R.degree-Q.degree, -1, -1):
			result[i] = R[i+Q.degree] / Q[Q.degree]
			R -= result.get_term(i) * Q
		
		result.trim_trailing_zeros()
		R.trim_trailing_zeros()
		
		return result, R
	
	def __floordiv__(self, other):
		return divmod(self, other)[0]
	def __rfloordiv__(self, other):
		return divmod(Polynomial[other], self)[0]
	
	def __truediv__(self, other):
		if type(other) is Polynomial:
			if other.degree == 0: return Polynomial(*reversed([c/other[0] for c in self]))
			else: raise ValueError("cannot divide by non constant poynomial")
		else: return Polynomial(*reversed([c/other for c in self]))
	def __rtruediv__(self, other):
		if self.degree == 0:
			raise NotImplementedError
		else: raise ValueError("cannot divide by non constant poynomial")
	
	def __mod__(self, other):
		return divmod(self, other)[1]
	def __rmod__(self, other):
		return divmod(Polynomial(other), self)[1]
	
	def __pow__(self, other: int, modulo=None):
		if type(other) is not int: raise TypeError
		if modulo is not None and type(modulo) is not Polynomial: modulo = Polynomial(modulo)
		P = Polynomial(1)
		for _ in range(other): P = P*self if modulo is not None else P*self % modulo
		return P
	
	def __call__(self, argument):
		if isinstance(argument, __import__("matrices").Matrix):
			raise NotImplementedError
		return sum(c*argument**i for i, c in enumerate(self))
	
	def derivative(self):
		return Polynomial(*reversed([i*self[i] for i in range(1,len(self))])).trim_trailing_zeros()
	
	def content(self):
		"""
		returns the content of the polynomial, or the GCD of all the coefficients.
		"""
		return basicfunctions.gcd_list(self.coefficients)
	
	def primitive_part(self):
		"""
		returns the primitive part of the polynomail.
		(The polynomial divided by its content)
		"""
		return self//self.content()
	
	def solve(self, precicion: int = 13) -> Tuple:
		"""
		returns the roots of the polynomial.
		"""
		if self.degree==0:
			return ()
		elif self.degree==1:
			a, b = self[1], self[0]
			return (-b/a,)
		elif self.degree==2:
			a, b, c = self[2], self[1], self[0]
			return ((-b+(b**2-4*a*c)**0.5)/(2*a), (-b-(b**2-4*a*c)**0.5)/(2*a))
		else:
			from math import log, ceil
			from cmath import exp, pi
			self_prime = self.derivative()
			d = self.degree
			
			R = 1+max(abs(self[i]/self.leading_coefficent) for i in range(self.degree))
			
			s = ceil(0.22632*log(d))
			N = ceil(8.32547*d*log(d))
			
			starting_points = []
			
			for v in range(s):
				rv = R*(((d-1)/d)**((2*v-1)/(4*s)))
				for i in range(N):
					starting_points.append(rv*exp((i*pi*2j)/N))
			
			roots = []
			for point in starting_points:
				x = point
				prev_x = float("NaN")
				while round(x.real, 13)!=round(prev_x.real, 13) or round(x.imag, 13)!=round(prev_x.imag, 13):
					prev_x = x
					x -= self(x)/self_prime(x)
				if self(x)!=0: complex(round(x.real, precicion), round(x.imag, precicion))
				roots.append(complex(round(x.real, precicion), round(x.imag, precicion))if round(x.imag, precicion)!=0 else round(x.real, precicion))
			
			return tuple(set(roots))
	
	@classmethod
	def from_roots(cls, *roots):
		P = cls(1)
		for r in roots: P = P * cls(1, -r)
		return P

def termwise_GCF(f: Polynomial) -> Polynomial:
	"""
	Returns the GCF of all of the terms in the polynomial.
	Example: 3x³+15x²+6x would return 3x.
	"""
	
	for i, c in enumerate(f):
		if c != 0: break
	GCF = Polynomial(type=f.type)
	GCF[i] = f.content()
	return GCF

def PolynomialGCD(A: Polynomial, B: Polynomial) -> Polynomial:
	"""
	Uses the pseudoremainder correction algorithm to compute the GCD of polynomials A and B.  
	
	e.g. GCD x³-7x-6 and x³+3x²-10x-24  
	would return x²-x-6  
	"""
	while True:
		# change if there is P.reduce_content()?
		A, B = B, (B.leading_coefficent**(A.degree-B.degree+1)*A)%B
		if B==0: return A//A.content()
		else: B//=B.content()

def rational_root_factor(f: Polynomial) -> Tuple[List[Polynomial], Polynomial]:
	"""
	Uses the rational root theorem to get all linear factors of the polynomial.  
	returns a list of the factors, and the remaining part of the polynomial that was not factored.  
	
	e.g. 14x⁸+63x⁷-182x⁶+217x⁵+1029x⁴-4900x³+2625x²+2646x or 7x(x+3)(x-2)(2x+1)(x²+5x-9)(x²-2x+7)  
	would return ([7x, x-2, x+3, 2x+1], x⁴+3x³-12x²+53x-63)
	"""
	P = f.copy()
	factors: List[Polynomial] = []
	
	gcf=termwise_GCF(P)
	if (gcf) != 1:
		factors.append(gcf)
		P//=gcf
	
	P.trim_trailing_zeros()
	
	for a in basicfunctions.factors(abs(P.leading_coefficent)):
		for b in basicfunctions.factors(abs(P[0])):
			for factor in (Polynomial(a, b), Polynomial(a, -b)):
				while P%factor==0:
					P//=factor
					factors.append(factor)
	
	return factors, P

def square_free_factor(f: Polynomial) -> Tuple[List[Polynomial], Polynomial]:
	"""
	Uses Yun's algorithm to get all repeated factors of a polynomial.
	This returns a tuple of a list of the factors it got and the unfactored part of the polynomial.
	
	e.g: x⁶-14x⁵+67x⁴-94x³-184x²+608x-384  
	would return ([x-4, x-4, x-4], x³-2x²-5x+6)
	"""
	A = f.copy()
	B = A.derivative()
	C = PolynomialGCD(f, f.derivative())
	
	squarefreefactors = []
	
	i = 1
	if C == 1:
		W = A
	else:
		W = A//C
		Y = B//C
		Z = Y - W.derivative()
		while Z != 0:
			G = PolynomialGCD(W, Z)
			if G!=1: squarefreefactors.append((i, G))
			i = i + 1
			W = W//G
			Y = Z//G
			Z = Y - W.derivative()
	
	squarefreefactors.append((i, W))
	
	factors = []
	leftover = Polynomial(1)
	for exp, p in squarefreefactors:
		if exp == 1: leftover = p
		else:
			for _ in range(exp):
				factors.append(p.copy())
	
	return factors, leftover

def is_prime(f: Polynomial[int]) -> bool:
	"""
	returns True if the given polynomial is irreducible over the integers.
	
	TODO: how tf should i do this
	"""
	raise NotImplementedError

if __name__=='__main__':
	# ¹²³⁴⁵⁶⁷⁸⁹⁰
	P = Polynomial.from_roots(-1, -1, -1)
	print(P)
	print(P.solve(precicion=4))