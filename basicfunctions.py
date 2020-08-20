"""
assorted widely useful functions on basic types.
"""
#TODO: maybe rewrite this whole library in C++ to make it super fast? idk

from typing import List
from functools import reduce

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
	from math import ceil,log2,log
	return any(any(i**k==n for k in range(2,ceil(log(n,i))+1))for i in range(2,ceil(log2(n))+1))

def is_prime(n: int) -> bool:
	"""
	Uses the AKS primality check to see if a number is prime.
	
	Complexity: O(log(n)^7)
	"""
	from math import floor,ceil,sqrt,log2
	
	if n==2: return True
	if n%2==0: return False
	
	if is_perfect_power(n): return False
	
	def get_r(n: int) -> int:
		l = log2(n)
		max_k, max_r = floor(l*l), max(3, ceil(l ** 5))
		
		next_r = True
		r = 1
		
		while(next_r and r<max_r):r,next_r=r+1,any(pow(n,k,r)in(0,1)for k in range(1,max_k))
		
		return r-1
	
	r = get_r(n)
	
	if n <= 5690034 and n <= r: return True
	
	if any(gcd(a,n)!=1 for a in range(1,r+1)): return False
	
	bound = floor(sqrt(φ(r))*log2(n))
	
	if any(pow(a,n,n)-a!=0 for a in range(1,bound+1)): return False
	
	return True

def sqrt_prime_check(n: int) -> bool:
	"""
	uses the naive square root check to determine if a number is prime.
	"""
	return not any(n%i==0 for i in range(2,int(__import__('math').sqrt(n)+1)))

def φ(n: int) -> int:
	"euler's totient function"
	#O(nlog(n))
	return sum(gcd(n, i)==1 for i in range(1, n))

def binomial_coefficient(n: int, k: int) -> int:
	"n choose k"
	# O(k)
	if k < 0: return 0
	if k == 0: return 1
	return int(reduce(lambda x, y: x * ((n+1-y)/y), range(1, k+1), 1))

if __name__ == "__main__":
	for x in range(10): print([binomial_coefficient(x, y) for y in range(10)])