import basicfunctions


class GroupMetaClass(type):
	"""
	meta class for all group classes.
	
	subclasses should impliment:
		identity (property)
	optional:
		__iter__, if you want to iterate over all elements of the group,
		__next__, also if you want to procedurally iterate over all elements of the group
	all other functions are optional as well.
	"""
	def __iter__(self): raise NotImplementedError
	def __next__(self): raise NotImplementedError
	@property
	def identity(self): raise NotImplementedError

class Group(metaclass=GroupMetaClass):
	"""
	Base class for all group objects.  
	Subclasses should implement:  
		Equality testing        (__eq__, ==)   
		Multiplication          (__mul__, *)  
		Multiplicative Inverse  (__invert__, ~)  
	Any other extra methods are optional.
	"""
	def __eq__(self, other) -> bool:
		raise NotImplementedError
	def __invert__(self):
		raise NotImplementedError
	def __mul__(self, other):
		raise NotImplementedError


class RingMetaClass(type):
	"""
	meta class for all ring classes.
	
	subclasses should impliment:
		additive identity (property)
		multiplicative identity (property)
	optional:
		__iter__, if you want to iterate over all elements of the ring,
		__next__, also if you want to procedurally iterate over all elements of the ring
	all other functions are optional as well.
	"""
	def __iter__(self): raise NotImplementedError
	def __next__(self): raise NotImplementedError
	@property
	def additive_identity(self): raise NotImplementedError
	@property
	def multipliative_identity(self): raise NotImplementedError

class Ring(metaclass=RingMetaClass):
	"""
	Base class for all ring objects.  
	Subclasses should implement:  
		Equality testing        (__eq__, ==)  
		Additive Inverse        (__neg__, -)  
		Addition                (__add__, +)  
		Multiplication          (__mul__, *)  
	Any other extra methods are optional, and subtraction is already implimented as adding its inverse.
	
	NOTE: in order to be used as an argument to a Polynomial object, it must impliment __pow__, with the second argument as an integer. (repeated multiplication works fine for this purpose.)
	"""
	def __eq__(self, other) -> bool:
		raise NotImplementedError
	def __neg__(self):
		raise NotImplementedError
	def __add__(self, other):
		raise NotImplementedError
	def __sub__(self, other):
		return self + (-other)
	def __mul__(self, other):
		raise NotImplementedError


class FieldMetaClass(RingMetaClass):
	"""
	meta class for all field classes.
	
	subclasses should impliment:
		additive identity (property)
		multiplicative identity (property)
	optional:
		__iter__, if you want to iterate over all elements of the field
		__next__, also if you want to procedurally iterate over all elements of the field
	all other functions are optional as well.
	"""
	def __iter__(self): raise NotImplementedError
	def __next__(self): raise NotImplementedError
	@property
	def additive_identity(self): raise NotImplementedError
	@property
	def multipliative_identity(self): raise NotImplementedError

class Field(Ring, metaclass=FieldMetaClass):
	"""
	Base class for all field objects.  
	Subclasses should implement:  
		Equality testing        (__eq__, ==)  
		Additive Inverse        (__neg__, -)  
		Multiplicative Inverse  (__invert__, ~)  
		Addition                (__add__, +)  
		Multiplication          (__mul__, *)  
	Any other extra methods are optional, and subtraction and division are already implimented as adding/multiplying by their inverses.
	
	NOTE:
	1. __inverse__ should raise a ZeroDivisionError on the additive identity of the field.  
	2. in order to be used as an argument to a Polynomial object, it must impliment __pow__, with the second argument as an integer. (repeated multiplication works fine for this purpose.)
	"""
	def __eq__(self, other) -> bool:
		raise NotImplementedError
	def __neg__(self):
		raise NotImplementedError
	def __invert__(self): #NOTE: this is the multiplicitive inverse
		raise NotImplementedError
	def __add__(self, other):
		raise NotImplementedError
	def __sub__(self, other):
		return self + (-other)
	def __mul__(self, other):
		raise NotImplementedError
	def __truediv__(self, other):
		return self * (~other)


class __ModularRingMetaClass(RingMetaClass):
	"""
	The Z/nZ ring metaclass.
	"""
	def __str__(self):
		return f"ModularRing[{self.modulus}]"
	def __repr__(self):
		return f"<class 'ModularRing'[{self.modulus}]>"
	def __eq__(self, other):
		return self.modulus==other.modulus
	def __iter__(self):
		self.iterindex=-1
		return self
	def __next__(self):
		self.iterindex+=1
		if self.iterindex>=self.modulus: raise StopIteration
		return self(self.iterindex)
	@property
	def additive_identity(self): return self(0)
	@property
	def multipliative_identity(self): return self(1)

class ModularRing(Ring, metaclass=__ModularRingMetaClass):
	"""
	the Z/nZ Ring.  
	NOTE: if n is prime, it is a field.
	
	Usage:  
	group = ModularRing[7]  
	element = group(5)  
	OR  
	element = ModularRing[7](5)  
	OR  
	element = ModularRing(5, modulus=7)
	"""
	modulus:int = None
	__is_field:bool = False
	
	def __class_getitem__(cls, key:int):
		cls.modulus = key
		cls.__is_field = basicfunctions.is_prime(key)
		return cls
	
	def __init__(self, value:int, modulus:int=None, __is_field:bool=None, **kwargs):
		if kwargs: raise KeyError
		if modulus is not None: self.modulus=modulus; self.__is_field = basicfunctions.is_prime(self.modulus)
		if __is_field is not None: self.__is_field=__is_field
		if self.modulus is None: raise ValueError("no modulus supplied for modular group instance")
		self.value = value % self.modulus
	
	def __int__(self) -> int:
		return self.value
	
	def __str__(self) -> str:
		return str(self.value)
	
	def __repr__(self) -> str:
		return f"ModularRing[{self.modulus}]({self.value})"
	
	def __eq__(self, other) -> bool:
		if type(other) is ModularRing: return self.value==other.value
		else: return self.value==other
	
	def __neg__(self):
		return ModularRing(-self.value%self.modulus, modulus=self.modulus, _ModularRing__is_field=self.__is_field)
	
	def __add__(self, other):
		if type(other) is ModularRing:
			if self.modulus!=other.modulus: raise ValueError
			return ModularRing((self.value+other.value)%self.modulus, modulus=self.modulus, _ModularRing__is_field=self.__is_field)
		elif type(other) is int: return ModularRing((self.value+other)%self.modulus, modulus=self.modulus, _ModularRing__is_field=self.__is_field)
		else: raise TypeError(f"expected int or Modular Ring Element, not {type(other).__name__}")
	def __radd__(self, other):
		if type(other) is int: return ModularRing((other+self.value)%self.modulus, modulus=self.modulus, _ModularRing__is_field=self.__is_field)
		else: raise TypeError(f"expected int or Modular Ring Element, not {type(other).__name__}")
	
	def __sub__(self, other):
		if type(other) is ModularRing:
			if self.modulus!=other.modulus: raise ValueError
			return ModularRing((self.value-other.value)%self.modulus, modulus=self.modulus, _ModularRing__is_field=self.__is_field)
		elif type(other) is int: return ModularRing((self.value-other)%self.modulus, modulus=self.modulus, _ModularRing__is_field=self.__is_field)
		else: raise TypeError(f"expected int or Modular Ring Element, not {type(other).__name__}")
	def __rsub__(self, other):
		raise NotImplementedError
	
	def __mul__(self, other):
		if type(other) is ModularRing:
			if self.modulus!=other.modulus: raise ValueError
			return ModularRing((self.value*other.value)%self.modulus, modulus=self.modulus, _ModularRing__is_field=self.__is_field)
		elif type(other) is int: return ModularRing((self.value*other)%self.modulus, modulus=self.modulus, _ModularRing__is_field=self.__is_field)
		else: raise TypeError(f"expected int or Modular Ring Element, not {type(other).__name__}")
	def __rmul__(self, other):
		if type(other) is int: return ModularRing((other*self.value)%self.modulus, modulus=self.modulus, _ModularRing__is_field=self.__is_field)
		else: raise TypeError(f"expected int or Modular Ring Element, not {type(other).__name__}")
	
	def __div__(self, other):
		raise NotImplementedError
	
	def __pow__(self, other):
		if type(other) is ModularRing:
			if self.modulus!=other.modulus: raise ValueError
			return ModularRing(pow(self.value, other.value, self.modulus), modulus=self.modulus, _ModularRing__is_field=self.__is_field)
		elif type(other) is int: return ModularRing(pow(self.value, other, self.modulus), modulus=self.modulus, _ModularRing__is_field=self.__is_field)
		else: raise TypeError(f"expected int or Modular Ring Element, not {type(other).__name__}")


class __F4MetaClass(FieldMetaClass):
	"""
	Example implimentation of the GF(4) field metaclass.
	"""
	def __iter__(self): return (self(i) for i in ('O', 'I', 'A', 'B'))
	def __next__(self): raise NotImplementedError
	@property
	def additive_identity(self):
		return self('O')
	@property
	def multipliative_identity(self):
		return self('I')

class F4(Field, metaclass=__F4MetaClass):
	"""
	Example implimentation of the GF(4) field.
	"""
	def __init__(self, value:str):
		if value not in ('O', 'I', 'A', 'B'): raise ValueError("F4 Elements are only 'O', 'I', 'A', and 'B'")
		self.value = value
	def __str__(self):
		return self.value
	def __repr__(self):
		return f"F4('{self.value}')"
	def __eq__(self, other) -> bool:
		return self.value==other.value
	def __neg__(self):
		return F4({'O':'O', 'I':'I', 'A':'A', 'B':'B'}[self.value])
	def __invert__(self):
		if self==self.__class__.additive_identity: raise ZeroDivisionError
		return F4({'O':None, 'I':'I', 'A':'B', 'B':'A'}[self.value])
	def __add__(self, other):
		return F4({
			'O': {'O':'O', 'I':'I', 'A':'A', 'B':'B'},
			'I': {'O':'I', 'I':'O', 'A':'B', 'B':'A'},
			'A': {'O':'A', 'I':'B', 'A':'O', 'B':'I'},
			'B': {'O':'B', 'I':'A', 'A':'I', 'B':'O'}
		}[self.value][other.value])
	def __mul__(self, other):
		return F4({
			'O': {'O':'O', 'I':'O', 'A':'O', 'B':'O'},
			'I': {'O':'O', 'I':'I', 'A':'A', 'B':'B'},
			'A': {'O':'O', 'I':'A', 'A':'B', 'B':'I'},
			'B': {'O':'O', 'I':'B', 'A':'I', 'B':'A'}
		}[self.value][other.value])


def test_group_axioms(group: Group):
	"""
	tests whether or not the given group satisfies all group axioms.  
	NOTE: the group must be iterable.
	"""
	assert(all(a*b in group for a in group for b in group)) # closure
	assert(all(a*(b*c)==(a*b)*c for a in group for b in group for c in group)) # associativity
	assert(all(a*group.identity==a for a in group)) # identity
	assert(all(a*(~a)==(~a)*a==group.identity for a in group)) # inverse

def test_ring_axioms(ring: Ring):
	"""
	tests whether or not the given ring satisfies all ring axioms.  
	NOTE: the ring must be iterable.
	"""
	assert(all(a+(b+c)==(a+b)+c for a in ring for b in ring for c in ring))
	assert(all(a+b==b+a for a in ring for b in ring))
	assert(all(a+ring.additive_identity==a for a in ring))
	assert(all(a+(-a)==ring.additive_identity for a in ring))
	
	assert(all(a*(b*c)==(a*b)*c for a in ring for b in ring for c in ring))
	assert(all(a*ring.multipliative_identity==a for a in ring))
	assert(all(a*(b+c)==a*b+a*c for a in ring for b in ring for c in ring))
	assert(all((a+b)*c==a*c+b*c for a in ring for b in ring for c in ring))

def test_field_axioms(field: Field):
	"""
	tests whether or not the given field satisfies all field axioms.  
	NOTE: the field must be iterable.
	"""
	assert(all(a+(b+c)==(a+b)+c for a in field for b in field for c in field))
	assert(all(a*(b*c)==(a*b)*c for a in field for b in field for c in field))
	
	assert(all(a+b==b+a for a in field for b in field))
	assert(all(a*b==b*a for a in field for b in field))
	
	assert(all(a+field.additive_identity==a for a in field))
	assert(all(a*field.multipliative_identity==a for a in field))
	
	assert(all(a+(-a)==field.additive_identity for a in field))
	assert(all(a==field.additive_identity or a*(~a)==field.multipliative_identity for a in field))
	
	assert(all(a*(b+c)==a*b+a*c for a in field for b in field for c in field))

if __name__ == "__main__":
	O, I, A, B = F4('O'), F4('I'), F4('A'), F4('B')
	
	print(A*B)