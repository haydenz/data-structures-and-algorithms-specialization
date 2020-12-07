# python3

import sys
from collections import namedtuple

Answer = namedtuple('answer_type', 'i j len')

def solve(s, t):
	ans = Answer(0, 0, 0)
	for i in range(len(s)):
		for j in range(len(t)):
			for l in range(min(len(s) - i, len(t) - j) + 1):
				if (l > ans.len) and (s[i:i+l] == t[j:j+l]):
					ans = Answer(i, j, l)
	return ans

class CommonSubstring:
	def __init__(self, s, t):
		self.s = s
		self.t = t
		self.len_s = len(s)
		self.len_t = len(t)
		self._prime1 = 100007
		self._prime2 = 100003
		self._multiplier = 87
		self.hash_s1 = self.hash_string(s, self._prime1)
		self.hash_s2 = self.hash_string(s, self._prime2)
		self.hash_t1 = self.hash_string(t, self._prime1)
		self.hash_t2 = self.hash_string(t, self._prime2)
		self.poly1 = self.precompute_poly(max(self.len_s, self.len_t)+1, self._prime1)
		self.poly2 = self.precompute_poly(max(self.len_s, self.len_t)+1, self._prime2)

	def solve(self):
		if self.s == self.t:
			return Answer(0,0,self.len_s)
		else:
			k = min(self.len_s, self.len_t)
			res = [None for _ in range(k+1)]
			str_l1 = []
			str_l2 = []
			left = 0
			right = k
			k = (left + right) // 2
			while k > 0:
				table_s1 = self.precompute_hash(k, self.s, self.hash_s1, self._prime1, self.poly1)
				table_s2 = self.precompute_hash(k, self.s, self.hash_s2, self._prime2, self.poly2)
				table_t1 = self.precompute_hash(k, self.t, self.hash_t1, self._prime1, self.poly1)
				table_t2 = self.precompute_hash(k, self.t, self.hash_t2, self._prime2, self.poly2)
				match1 = self.match(table_s1, table_t1, k)
				match2 = self.match(table_s2, table_t2, k)
				ans = self.find(match1, match2)
				if len(ans) != 0: #TODO
					# return ans[0]
					res[k] = True
					if k == min(self.len_s, self.len_t):
						return ans[0]
					elif res[k+1] == False:
						return ans[0]
					left = k
					k = (left + right) // 2
				else:
					res[k] = False
					right = k
					k = (left + right) // 2
		return Answer(0,0,0)
	
	def match(self, l1, l2, k):
		res = []
		for i in range(len(l1)):
			if l1[i] in l2:
				res.append(Answer(i,l2.index(l1[i]),k))
		return res

	def find(self, l1, l2):
		return [l for l in l1 if l in l2]

	def hash_string(self, text, _prime):
		text_len = len(text)
		hash_l = [-1] * (text_len+1)
		hash_l[0] = 0
		for i in range(1, text_len+1):
			hash_l[i] = (hash_l[i-1]*self._multiplier+ord(text[i-1]))%_prime
		return hash_l
	
	def precompute_hash(self, k, text, hash_l, _prime, poly):
		res = []
		for i in range(0, len(text)-k+1):
			res.append((hash_l[i+k]-poly[k]*hash_l[i])%_prime)
		return res

	def precompute_poly(self, l, _prime):
		res = []
		for i in range(l):
			res.append(pow(self._multiplier, i, _prime))
		return res

if __name__ == '__main__':
	for line in sys.stdin.readlines():
		s, t = line.split()
		solver = CommonSubstring(s, t)
		ans = solver.solve()
		print(ans.i, ans.j, ans.len)
