"""
assorted widely useful functions on basic types.
"""
#TODO: maybe rewrite this whole library in C++ to make it super fast

from typing import List
from functools import reduce
from math import ceil, floor, log2, sqrt

def gcd(a: int, b: int) -> int:
    # O(log(a)+log(b))
    if a < 0 or b < 0:
        raise ValueError("arguments to gcd() cannot be less than 0")
    if a + b in [a, b]:
        return a + b
    return gcd(a % b, b) if a > b else gcd(a, b % a)

def gcd_list(l: List[int]) -> int:
	return reduce(gcd, l)

def lcm(a: int, b: int) -> int:
	# O(log(a)+log(b))
	return (a * b) // gcd(a, b)

def prime_factors(n: int) -> list:
	# O(n)
	factors = []
	i = 2
	while n != 1:
		if n % i == 0:
			factors.append(i)
			n = n / i
		else:
			i += 1
	return factors

def factors(n: int) -> list:
	# O(n)
	return [i for i in range(1, n + 1) if not n % i]

def is_perfect_power(n: int) -> bool:
	"""
	tests if n is a perfect power.  
	e.g:  
	is_perfect_power(125) -> True  
	is_perfect_power(69) -> False  
	"""
	# O(log(n))
	for i in range(2, ceil(log2(n))+1): 
		if not n ** (1 / i) % 1:
			return True
	return False

def is_prime(n: int) -> bool:
	"""
	Uses the AKS primality check to see if a number is prime.
	
	Complexity: O(log(n)^7)
	"""
	
	if n == 2: return True
	
	if n % 2 == 0: return False
	
	if is_perfect_power(n): return False
	
	def get_r(n: int) -> int:
		l = log2(n)
		max_k = floor(l*l)
		max_r = max(3, ceil(l ** 5))
		
		next_r = True
		
		r = 2
		
		while (next_r and r < max_r):
			next_r = False
			
			k = 1
			
			while not next_r and k < max_k:
				next_r = pow(n, k, r) in (0, 1)
				
				k = k + 1
			
			r = r + 1
		
		return r - 1
	
	r = get_r(n)
	
	if n <= 5690034 and n <= r: return True
	
	for a in range(r, 0, -1):
		if gcd(a, n) != 1: return False
	
	bound = floor(sqrt(φ(r)) * log2(n))
	
	for a in range(1, bound+1):
		if pow(a, n, n) - a != 0: return False
	
	return True

def φ(n: int) -> int:
	#O(nlog(n))
	return sum(gcd(n, i) == 1 for i in range(1, n))

def binomial_coefficient(n: int, k: int) -> int:
	# O(k)
	if k < 0: return 0
	if k == 0: return 1
	return int(reduce(lambda x, y: x * ((n+1-y)/y), range(1, k+1), 1))

if __name__ == "__main__":
	for x in range(10): print([binomial_coefficient(x, y) for y in range(10)])