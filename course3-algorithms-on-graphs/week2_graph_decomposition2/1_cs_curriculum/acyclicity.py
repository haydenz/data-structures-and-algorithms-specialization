#Uses python3

import sys

clock = 1

class Vertex:
    def __init__(self, x):
        self.key = x
        self.adj = []
        self.visited = False
        self.stack = False

class Graph:
    def __init__(self, adj, n):
        self.adj = adj
        self.n = n
        self.vertices = self.create_graph(self.adj)

    def create_graph(self, adj):
        vertices = [None for i in range(n)]
        for i in range(self.n):
            vertices[i] = Vertex(i)
        for i in range(n):
            for _, a in adj[i]:
                vertices[i].adj.append(vertices[a])
        return vertices

    def explore(self, v):
        # Mark current node as visited
        v.visited = True
        # Add to recursion stack
        v.stack = True
        # For all neighbors of current node, 
        # if any neighbor is visited and in the
        # recursion stack, then the graph contains circle
        for w in v.adj:
            if not w.visited:
                if self.explore(w):
                    return True
            elif w.stack:
                return True
        v.stack = False
        return False

    def is_cyclic(self):
        for v in self.vertices:
            if not v.visited:
                if self.explore(v):
                    return 1
        return 0

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append((a-1, b-1))
    directed_graph = Graph(adj, n)
    print(directed_graph.is_cyclic())
