from typing import Union, List, Tuple, Any
from functools import reduce
from polynomials import Polynomial
from fractions import Fraction

class Matrix:
	"""
	TODO
	"""
	
	def __class_getitem__(cls, key:type):
		if type(key) is not type: raise TypeError("Parameters to generic types must be types. Got {thing}.".format(thing=key))
		cls.type = key
		raise NotImplementedError
		return cls
	
	@classmethod
	def Identity(cls, size: int):
		return cls([[int(i==j) for j in range(size)] for i in range(size)])
	
	@classmethod
	def NullMatrix(cls, size: Union[Tuple[int], int]):
		if type(size) is tuple: return cls([[0 for _ in range(size[1])] for _ in range(size[0])])
		else: return cls([[0 for _ in range(size)] for _ in range(size)])
	
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
		else:
			if not all(isinstance(l, (list, tuple)) for l in value) and not len(value)==0: raise TypeError("expected a list of lists for matrix creation")
			self.list = value
			self.type = type
			num_rows = len(self.list)
			num_columns = len(self.list[0]) if num_rows > 0 else 0
			for i in self.list:
				if len(i)!=num_columns: raise ValueError("attempted to use a non-rectangular matrix")
			if self.type is not Any:
				for row in self.list:
					for i, item in enumerate(row):
						if item!=0:
							try: row[i] = self.type(item)
							except: raise TypeError(f"{item} is not of type {self.type.__name__}")
			self.rows, self.columns = num_rows, num_columns
	
	@property
	def dimensions(self) -> Tuple[int]:
		return (self.rows, self.columns)
	
	@property
	def is_square(self) -> bool:
		return self.rows==self.columns
	
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
		if isinstance(indices[0], int) and isinstance(indices[1], int):
			return self.list[indices[0]][indices[1]]
		elif isinstance(indices[0], slice) or isinstance(indices[1], slice):
			if isinstance(indices[0], slice):
				row_start = indices[0].start
				row_stop = indices[0].stop
				row_step = indices[0].step
			elif isinstance(indices[0], int):
				row_start = indices[0]
				row_stop = indices[0]+1
				row_step = 1
			else: raise TypeError
			if isinstance(indices[1], slice):
				column_start = indices[1].start
				column_stop = indices[1].stop
				column_step = indices[1].step
			elif isinstance(indices[1], int):
				column_start = indices[1]
				column_stop = indices[1]+1
				column_step = 1
			else: raise TypeError
			
			if row_step is None: row_step = 1
			if column_step is None: column_step = 1
			if row_start is None: row_start = 0 if row_step>0 else self.dimensions[0]-1
			if row_stop is None: row_stop = self.dimensions[0] if row_step>0 else -1
			if column_start is None: column_start = 0 if column_step>0 else self.dimensions[1]-1
			if column_stop is None: column_stop = self.dimensions[1] if column_step>0 else -1
			
			A = Matrix((abs(row_stop-row_start), abs(column_stop-column_start)))
			
			for i in range(row_start, row_stop, row_step):
				for j in range(column_start, column_stop, column_step):
					A[abs(i-row_start), abs(j-column_start)] = self[i,j]
			
			return A
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
		return reduce(lambda x, y: x*y, [self[i,i] for i in range(min(self.dimensions))], 1)
	
	def trace(self):
		"""computes the diagonal sum of a given matrix. also the sum of the eigenvalues of the matrix."""
		return reduce(lambda x, y: x+y, [self[i,i] for i in range(min(self.dimensions))])
	
	def __row_echelon_determinant(self) -> Tuple:
		"""
		returns the row-echelon form and determinant of the matrix.
		"""
		A = self.copy()
		d = 1
		
		for i in range(A.rows):
			#get row with nonzero i-th entry and swap it with row i
			if i < A.columns and A[i,i]==0:
				for r in range(i, A.columns):
					if A[i,r]!=0:
						A.swap(i, r)
						d*=-1
						break
			
			# gets leftmost nonzero column
			column = None
			for col in range(A.columns):
				if not all(A.list[row][col]==0 for row in range(i, A.rows)):
					column = col
					break
			if column is None: break
			
			d*=A[i, column]
			A.list[i] = [num/A[i, column] for num in A.list[i]] # god i fucking hate floats
			
			for i2 in range(i+1, A.rows):
				A.add_multiply_two_rows(i2, i, -A[i2, column])
		
		try:
			if all(A[i,j]==round(A[i,j]) for i in range(A.rows) for j in range(A.columns)):
				for i in range(A.rows):
					for j in range(A.columns): A[i,j]=int(A[i,j])
		except TypeError: pass
		
		return A, A.diagonal_product()*d
	
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
		if any(isinstance(self[i,j], Polynomial) for i in range(self.rows) for j in range(self.columns)):
			#TODO: if the polynomial has floats, the tiny errors grow huge and destroy the whole thing.
			A = self.copy()
			d = 1
			
			i, j, m, n = 0, 0, A.columns, A.rows
			
			while i < m and j < n:
				if all(A[k,j]==0 for k in range(i, m)): j = j + 1
				else:
					while not all(A[k,j]==0 for k in range(i+1, m)):
						#get minimal degree polynomial in column
						min_deg = float('inf')
						addr = None
						for k in range(i, m):
							if A[k,j].degree <= min_deg:
								min_deg, addr = A[k,j].degree, k
						
						if i != addr: A.swap(i, addr); d = -d
						
						for k in range(i+1, A.rows): A.add_multiply_two_rows(k, j, -A[k,j]//A[j,j])
					
					i, j = i+1, j+1
			
			return A.diagonal_product() * d
		else: return self.__row_echelon_determinant()[1]
	
	def rank(self) -> int:
		"""returns the rank of the matrix."""
		return sum(not self.reduced_row_echelon_form().is_zero_row(i) for i in range(self.rows))
	
	def nullity(self) -> int:
		"""returns the nullity of the matrix."""
		return sum(self.reduced_row_echelon_form().is_zero_row(i) for i in range(self.rows))
	
	def inverse(self):
		if self.is_square: return self.augment(Matrix.Identity(self.dimensions[0])).reduced_row_echelon_form()[:,self.dimensions[0]:]
		else: raise ValueError("TODO: find pseudoinverses of nonsquare matrices")
	
	def minor_matrix(self, row: int, column: int):
		"""returns a matrix without given row and column."""
		return Matrix([row[:column] + row[column+1:] for row in (self.list[:row]+self.list[row+1:])])
	
	def cofactor(self, row: int, column: int):
		"""returns the cofactor for a given row and column."""
		return ((-1)**(row+column)) * self.minor_matrix(row, column).determinant()
	
	def cofactor_matrix(self):
		"""returns the cofactor matrix for a given matrix."""
		return Matrix([[self.cofactor(i, j) for j in range(self.columns)] for i in range(self.rows)])
	
	def transpose(self):
		"""returns the transpose matrix of given matrix."""
		return Matrix([[self[j,i] for j in range(self.columns)] for i in range(self.rows)])
	
	def __add__(self, other):
		if self.dimensions != other.dimensions: raise ValueError(f"matrices do not have same dimensions [{self.dimensions} and {other.dimensions}]")
		return Matrix([[self[i,j]+other[i,j] for j in range(self.columns)] for i in range(self.rows)], type=self.type if self.type is other.type else Any)
	
	def __sub__(self, other):
		if self.dimensions != other.dimensions: raise ValueError(f"matrices do not have same dimensions [{self.dimensions} and {other.dimensions}]")
		return Matrix([[self[i,j]-other[i,j] for j in range(self.columns)] for i in range(self.rows)], type=self.type if self.type is other.type else Any)
	
	def __mul__(self, other):
		if isinstance(other, Matrix):
			if self.columns != other.rows: raise ValueError(f"matrices do not have correct dimensions [{self.dimensions} and {other.dimensions}]")
			return Matrix([[sum(self[i,n]*other[n,j] for n in range(self.columns)) for j in range(other.columns)] for i in range(self.rows)], type=self.type if self.type is other.type else Any)
		else: return Matrix([[self[i,j]*other for j in range(self.columns)] for i in range(self.rows)], type=self.type)
	def __rmul__(self, other):
		return Matrix([[other*self[i,j] for j in range(self.columns)] for i in range(self.rows)], type=self.type)
	
	def __pow__(self, other: int):
		#TODO: convert to eigenbasis and then do power and then go back, much faster
		if not self.is_square: raise ValueError("cannot raise nonsquare matrices to a power")
		A = Matrix.Identity(self.dimensions[0])
		for _ in range(other): A = A * self
		return A
	
	def characteristic_polynomial(self) -> Polynomial:
		return (self.cast(Polynomial[Fraction])-Matrix.Identity(self.dimensions[0])*Polynomial(1,0)).determinant()
	
	def eigenvalues(self) -> Tuple:
		return self.characteristic_polynomial().solve()
	
	def eigenvectors(self) -> List:
		raise NotImplementedError
	
	def eigenpairs(self):
		raise NotImplementedError

if __name__=='__main__':
	
	A = Matrix([[3, 2], [4, 1]])
	
	print(A.characteristic_polynomial(), A.eigenvalues())