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
		if len(s) <= len(t):
			self.s = s
			self.t = t
			self.flag = True
		else:
			self.s = t
			self.t = s
			self.flag = False
		self.len_s = len(self.s)
		self.len_t = len(self.t)
		self._prime1 = 1000000007
		self._prime2 = 1000000009
		self._multiplier = 113
		self.hash_s1 = self.hash_string(self.s, self._prime1)
		self.hash_s2 = self.hash_string(self.s, self._prime2)
		self.hash_t1 = self.hash_string(self.t, self._prime1)
		self.hash_t2 = self.hash_string(self.t, self._prime2)
		self.poly1 = self.precompute_poly(self.len_t + 1, self._prime1)
		self.poly2 = self.precompute_poly(self.len_t + 1, self._prime2)

	def solve(self):
		if self.s == self.t:
			return Answer(0,0,self.len_s)
		else:
			k = self.len_s
			res = [None for _ in range(k+1)]
			str_l1 = []
			str_l2 = []
			left = 0
			right = k
			# k = (left + right) // 2
			while k > 0:
				hash_dict_s1 = self.precompute_hash(k, self.s, self.hash_s1, self._prime1, self.poly1)
				hash_dict_s2 = self.precompute_hash(k, self.s, self.hash_s2, self._prime2, self.poly2)
				match1 = self.match_hash(hash_dict_s1, k, self.t, self.hash_t1, self._prime1, self.poly1)
				match2 = self.match_hash(hash_dict_s2, k, self.t, self.hash_t2, self._prime2, self.poly2)
				ans = self.find(match1, match2)
				if len(ans) != 0:
					res[k] = True
					if k == min(self.len_s, self.len_t):
						return ans[-1]
					elif res[k + 1] == False:
						return ans[-1]
					left = k + 1
					k = (left + right) // 2
				else:
					res[k] = False
					right = k - 1
					k = (left + right) // 2
		return Answer(0,0,0)
	
	def match_hash(self, hash_dict, k, text, hash_l, _prime, poly):
		res = []
		for i in range(0, len(text) - k + 1):
			tmp = (hash_l[i + k] - poly[k] * hash_l[i]) % _prime
			try:
				pos = hash_dict[tmp]
				if self.flag:
					res.append(Answer(pos, i, k))
				else:
					res.append(Answer(i, pos, k))
			except KeyError:
				continue
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
		res = dict()
		for i in range(0, len(text) - k + 1):
			res.update({((hash_l[i + k] - poly[k] * hash_l[i]) % _prime) : i})
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
