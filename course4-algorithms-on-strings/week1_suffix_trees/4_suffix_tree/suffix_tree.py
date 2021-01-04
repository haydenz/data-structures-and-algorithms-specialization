# python3
import sys

class Vertex:
	def __init__(self, label):
		self.pattern_end = False
		self.label = label
		self.edges = dict()

def build_trie(patterns, n):
	tree, label = dict(), -1
	root = Vertex(label)
	for pattern in patterns:
		curr_node = root
		pattern_end = False
		for i in range(len(pattern)):
			curr_symbol = pattern[i]
			if i == len(pattern) - 1:
				pattern_end = True
			try:
				if tree[curr_node.label][curr_symbol].pattern_end:
					pattern_end = True
			except Exception as e:
				pass

			if bool(curr_node.edges) and curr_symbol in curr_node.edges:
				curr_node = curr_node.edges[curr_symbol]
				curr_node.pattern_end = pattern_end
			else:
				if pattern_end:
					new_node = Vertex(n - len(pattern))
				else:
					label += -1
					new_node = Vertex(label)
				new_node.pattern_end = pattern_end
				curr_node.edges.update({curr_symbol: new_node})
				tree.update({curr_node.label: curr_node.edges})
				curr_node = new_node
	return root

def compress(trie):
  #
  pass

def build_suffix_tree(text):
  """
  Build a suffix tree of the string text and return a list
  with all of the labels of its edges (the corresponding 
  substrings of the text) in any order.
  """
  result = []
  # Implement this function yourself
  patterns = []
  for i in range(len(text)):
    patterns.append(text[i:])
  v = build_trie(patterns, len(text))
  while bool(v.edges):
    pass

  return result


if __name__ == '__main__':
  text = sys.stdin.readline().strip()
  result = build_suffix_tree(text)
  print("\n".join(result))