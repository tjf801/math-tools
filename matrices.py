from typing import Union, List, Tuple, Any

class Matrix:
	"""
	TODO
	"""
	
	def __class_getitem__(cls, key:type):
		if type(key) is not type: raise TypeError("Parameters to generic types must be types. Got {thing}.".format(thing=key))
		cls.type = key
		return cls
	
	def __init__(self, value: Union[List, Tuple], type:type=Any):
		"""
		Creates a matrix, either from a list of its values, or a list of its dimensions.
		
		Example usage:  
		#creates the matrix from the list  
		A = Matrix([[1, 2, 3], [4, 5, 6]])
		
		# creates a 3x3 null matrix from the dimensions
		B = Matrix([3, 3])
		"""
		if len(value)==2 and isinstance(value[0], int) and isinstance(value[1], int):
			# create from dimensions
			self.list = [[0 for _ in range(value[1])] for _ in range(value[0])]
			self.type = type
			self.rows, self.columns = value[0], value[1]
			self.is_square = self.rows==self.columns
		else:
			if not all(isinstance(l, (list, tuple)) for l in value): raise TypeError("expected a list of lists for matrix creation")
			self.list = value
			self.type = type
			num_rows = len(self.list)
			num_columns = len(self.list[0])
			for i in self.list:
				if len(i)!=num_columns: raise ValueError("attempted to use a non-rectangular matrix")
			if self.type is not Any:
				for row in self.list:
					for item in row:
						if item!=0 and not isinstance(item, self.type):
							try: item = self.type(item)
							except: raise TypeError(f"{item} is not of type {self.type.__name__}")
			self.rows, self.columns = num_rows, num_columns
			self.is_square = self.rows==self.columns
	
	@property
	def dimensions(self) -> tuple:
		return (self.rows, self.columns)
	
	def copy(self):
		"""
		returns a copy of a matrix.
		"""
		#why can't python assignment be normal
		return Matrix([[self[i,j] for j in self.columns] for i in self.rows])
	
	def cast(self, type:type):
		return Matrix([[type(item) for item in row] for row in self.list], type=type)
	
	def __list__(self) -> list:
		return self.list
	
	def __getitem__(self, indices:Union[Tuple[int], Tuple[slice]]):
		if isinstance(indices[0], int):
			return self.list[indices[0]][indices[1]]
		elif isinstance(indices[0], slice):
			raise NotImplementedError #TODO
		else: raise TypeError(f"Matrix indices must be integers or slices, not {type(indices[0].__name__)}")
	
	def __setitem__(self, indices:Tuple[int], value):
		#TODO: slice support?
		self.list[indices[0]][indices[1]] = value
	
	def __eq__(self, other) -> bool:
		if type(other) is not Matrix: return False
		if self.dimensions != other.dimensions: return False
		return all([[self[i,j]==other[i,j] for j in self.columns] for i in self.rows])
	
	

if __name__=='__main__':
	A = Matrix([[1, 2], [3, 4]])
	print(A[1,1])