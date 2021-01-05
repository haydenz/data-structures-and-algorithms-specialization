# python3
import sys

SYMBOL1 = "#"
SYMBOL2 = "$"

class SuffixTree:
	class Vertex:
		def __init__(self, label):
			self.label = label
			self.edges = dict()
			self.text1 = False
			self.pos = None
	
	def __init__(self, text, len_p):
		""" Make suffix tree, without suffix links, 
		from s in quadratic time and linear space """
		self.root = self.Vertex(None)
		self.root.pos = (0, len(text))
		self.text = text
		all_text = self.Vertex(text)
		all_text.pos = (0, len(text))
		if text[0] != SYMBOL1:
			all_text.text1 = True
		self.root.edges[text[0]] =  all_text# trie for just longest suffix
        # Add rest suffixes, from longest to shortest
		for i in range(1, len(text)):
            # start at root; we’ll walk down as far as we can go
			cur_node = self.root
			j = i
			while j < len(text):
				if text[j] in cur_node.edges:
					child = cur_node.edges[text[j]]
					label = child.label
					# if not child.text1:
					child.text1 = True if j <= len_p else False
                    # Walk along edge until we exhaust edge label or
                    # until we mismatch
					k = j+1 
					while k-j < len(label) and text[k] == label[k-j]:
						k += 1
					if k-j == len(label):
						cur_node = child # we exhausted the edge
						j = k
					else:
                        # we fell off in middle of edge
						cExist, cNew = label[k-j], text[k]
                        # create “mid”: new node bisecting edge
						mid = self.Vertex(label[:k-j])
						mid.pos = (child.pos[0], len(label[:k-j]))
						mid.text1 = child.text1
					
						tmp = self.Vertex(text[k:])
						tmp.text1 = True if k <= len_p else False
						tmp.pos = (k, len(text[k:]))
						
						mid.edges[cNew] = tmp
                        # original child becomes mid’s child
						mid.edges[cExist] = child
                        # original child’s label is curtailed
						child.label = label[k-j:]
						child.pos = (child.pos[0]+k-j, len(label[k-j:]))
						child.text1 = True if child.pos[0] <= len_p else False
						cur_node.edges[text[j]] = mid
				else:
					# Fell off tree at a node: make new edge hanging off it
					new_node = self.Vertex(text[j:])
					if j <= len_p:
						new_node.text1 = True
					else:
						cur_node.text1 = False
					new_node.pos = (j, len(text[j:]))
					cur_node.edges[text[j]] = new_node

	def max_label(self):
		current = self.root
		stack, res = [], []
		while True:
			if bool(current.edges):
				k = list(current.edges.keys())[0]
				if bool(current.edges[k].edges) or current.edges[k].text1:
					stack.append(current.edges[k])
				del current.edges[k]
			elif stack:
				current = stack.pop()
				if current.text1:
					pos, length = current.pos
					if current.label[0] == SYMBOL1:
						res.append(self.text[pos:pos+1])
					else:
						res.append(self.text[pos:pos+1])
			else:
				break
		return min(res, key=len)	
	
	def path(self, node):
		pass

def solve(p, q):
	tree = SuffixTree(p+SYMBOL1+q+SYMBOL2, len_p=len(p))
	return tree.max_label()

if __name__ == '__main__':
	p = sys.stdin.readline ().strip ()
	q = sys.stdin.readline ().strip ()
	ans = solve(p, q)
	sys.stdout.write (ans + '\n')
