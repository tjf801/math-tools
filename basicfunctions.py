"""
assorted widely useful functions on basic types.
"""
#TODO: maybe rewrite this whole library in C++ to make it super fast? idk

from typing import List
from functools import reduce
import cmath

def gcd(a: int, b: int) -> int:
	# O(log(a)+log(b))
	while True:
		if a==0: return b
		if b==0: return a
		if abs(a) > abs(b): a %= b
		else: b %= a

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
	
	if any(gcd(a,n)!=1 for a in range(1,r+1)): return False
	
	if n <= 5690034 and n <= r: return True
	
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

def FFT(P: list):
	n = len(P)
	if __import__("math").log2(n)!=round(__import__("math").log2(n)):
		raise ValueError("args to FFT() need to be of dimension 2^n")
	if n==1: return P
	omega = cmath.exp(2j*cmath.pi/n)
	P_even, P_odd = P[::2], P[1::2]
	y_even, y_odd = FFT(P_even), FFT(P_odd)
	y = [y_even[j] + omega**j * y_odd[j] for j in range(n//2)] + [y_even[j] - omega**j * y_odd[j] for j in range(n//2)]
	return y

def IFFT(y: list):
	return [x.conjugate()/len(y) for x in FFT([x.conjugate() for x in y])]

if __name__ == "__main__":
	print(FFT([0, 1, 1, 3]))