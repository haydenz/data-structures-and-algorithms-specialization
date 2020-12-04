# python3

import sys

class Solver:
	_multiplier = 5
	_prime = 1000003

	def __init__(self, text):
		self.text = text
		self.text_len = len(text)
		self.hash_l = None

	def ask(self, a, b, l):
		# return self.text[a:a+l] == self.text[b:b+l]
		poly = 1
		for i in range(1, l + 1):
			poly = (poly * self._multiplier) % self._prime
		return self.fast_hash(a, l, poly) == self.fast_hash(b, l, poly)
	
	def fast_hash(self, a, l, poly):
		hash1 = self.poly_hash(self.text[:a+l])
		hash2 = self.poly_hash(self.text[:a])
		return hash1-poly*hash2
   
	def poly_hash(self, s):
		ans = 0
		for c in reversed(s):
			ans = (ans * self._multiplier + ord(c)) % self._prime # ord() returns Unicode char
		return ans

s = sys.stdin.readline()
q = int(sys.stdin.readline())
solver = Solver(s)
for i in range(q):
	a, b, l = map(int, sys.stdin.readline().split())
	print("Yes" if solver.ask(a, b, l) else "No")
