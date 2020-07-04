import basicfunctions


class Group: pass

class Ring(Group): pass

class Field(Ring): pass


class __ModularRingMetaClass(type):
	def __str__(self):
		return f"ModularRing[{self.modulus}]"
	def __repr__(self):
		return f"<class 'ModularRing'[{self.modulus}]>"
	def __eq__(self, other):
		return self.modulus==other.modulus
	def __iter__(self):
		self.iterindex = -1
		return self
	def __next__(self):
		self.iterindex+=1
		if self.iterindex>=self.modulus: raise StopIteration
		return self(self.iterindex)

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

if __name__ == "__main__":
	ModularRing[5](4) # returns 4 mod 5
	
	G = ModularRing[7] # the group Z/7Z
	
	print([a for a in G])