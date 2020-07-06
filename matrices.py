from typing import Union, List, Tuple, Any
from functools import reduce

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
		return Matrix([[self[i,j] for j in range(self.columns)] for i in range(self.rows)], type=self.type)
	
	def cast(self, type:type):
		return Matrix([[type(item) for item in row] for row in self.list], type=type)
	
	def __repr__(self) -> str:
		return f"Matrix{'<' + self.type.__name__ + '>' if self.type is not Any else ''}({self.list})"
	
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
	
	def augment(self, other):
		"""augments a matrix with another."""
		if self.rows != other.rows: raise ValueError("Cannot augment two matrices with different amounts of rows")
		return Matrix([[item for item in self.list[i]+other.list[i]] for i in range(self.rows)], type=self.type if self.type is other.type else Any)
	
	def vertical_augment(self, other):
		if self.columns != other.columns: raise ValueError("Cannot vertically augment two matrices with different amounts of columns")
		return Matrix(self.list + other.list)
	
	def swap(self, r1: int, r2: int):
		"""swaps the given two rows"""
		self.list[r1], self.list[r2] = self.list[r2], self.list[r1]
	
	def multiply_row_by_scalar(self, row: int, num):
		"""multiplies a given row by a scalar."""
		self.list[row] = [num*i for i in self.list[row]]
	
	def add_multiply_two_rows(self, r1, r2, a):
		"""performs the operation r1 += a*r2"""
		self.list[r1] = [ self.list[r1][i] + a*self.list[r2][i] for i in range(self.columns)]
	
	def index_of_leading_term(self, row: int) -> int:
		"""
		returns the index of the leading term for a given row.
		if the row is all zeros, it returns None.
		"""
		for i, n in enumerate(self.list[row]):
			if n!=0: return i
		return None
	
	def is_zero_row(self, row: int) -> bool:
		"""tests if a given row is completely full of zeros."""
		return all(self.list[row][i]==0 for i in range(self.columns))
	
	def is_zero_column(self, column: int) -> bool:
		"""tests if a given column is completely full of zeros."""
		return all(self.list[i][column]==0 for i in range(self.rows))
	
	def diagonal_product(self):
		"""returns the product of the main diagonal of a matrix. used when computing the determinant."""
		return reduce(lambda x, y: x*y, [self[i,i] for i in range(min(self.dimensions))])
	
	def trace(self):
		"""computes the diagonal sum of a given matrix. also the sum of the eigenvalues of the matrix."""
		return reduce(lambda x, y: x+y, [self[i,i] for i in range(min(self.dimensions))])
	
	def __row_echelon_determinant(self):
		"""
		returns the row-echelon form and determinant of a given matrix.
		if return_determinant is True, it returns the determinant of the matrix instead, because it uses the exact same algorithm.
		"""
		A = self.copy()
		d = 1
		
		for i in range(A.rows):
			#get row with nonzero i-th entry and swap it with row i
			if i < A.columns and A[i,i]==0:
				for r in range(i, A.columns):
					if A[i,r]!=0:
						A.swap(i, r)
						d *= -1
						break
			
			# gets leftmost nonzero column
			column = None
			for col in range(A.columns):
				if not all(A.list[row][col]==0 for row in range(i, A.rows)):
					column = col
					break
			if column is None: break
			
			d *= A[i, column]
			A.list[i] = [num/A[i, column] for num in A.list[i]] # god i fucking hate floats
			
			for i2 in range(i+1, A.rows):
				A.add_multiply_two_rows(i2, i, -A[i2, column])
		
		try:
			if all(A[i,j]==round(A[i,j]) for i in range(A.rows) for j in range(A.columns)):
				for i in range(A.rows):
					for j in range(A.columns): A[i,j]=int(A[i,j])
		except TypeError: pass
		
		return A, d * A.diagonal_product()
	
	def row_echelon_form(self):
		return self.__row_echelon_determinant()[0]
	
	def reduced_row_echelon_form(self):
		"""returns the reduced row-echelon form of the given matrix."""
		A = self.row_echelon_form()
		for i in range(min(A.dimensions)-2, -1, -1): # min(A.dimensions)
			for j in range(min(A.dimensions)-1, i, -1):
				if not A.is_zero_row(j): A.add_multiply_two_rows(i, j, -A[i, A.index_of_leading_term(j)])
		try:
			if all(A[i,j]==round(A[i,j]) for i in range(A.rows) for j in range(A.columns)):
				for i in range(A.rows):
					for j in range(A.columns): A[i,j]=int(A[i,j])
		except TypeError: pass
		
		return A
	
	def determinant(self):
		return int(self.__row_echelon_determinant()[1]) if self.type is int else self.__row_echelon_determinant()[1]
	
	def rank(self) -> int:
		"""returns the rank of the matrix."""
		return sum(not self.reduced_row_echelon_form().is_zero_row(i) for i in range(self.rows))
	
	def nullity(self) -> int:
		"""returns the nullity of the matrix."""
		return sum(self.reduced_row_echelon_form().is_zero_row(i) for i in range(self.rows))

if __name__=='__main__':
	A = Matrix([[-7 , -1 , -5 , 2], [10 , -3 , -8 , 10], [-2 , -10 , 1 , 2]], type=int)
	print(A.reduced_row_echelon_form())