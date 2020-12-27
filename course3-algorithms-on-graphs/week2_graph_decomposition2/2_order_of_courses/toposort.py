#Uses python3

import sys


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
            for a in adj[i]:
                vertices[i].adj.append(vertices[a])
        return vertices
    
    def find_sink(self):
        for v in self.vertices:
            if not v.visited:
                v.visited = True
                if len(v.adj) == 0:
                    return v.key
        return -1

    def delete_vertex(self, v_idx):
        adj = self.adj
        for i, a in enumerate(adj):
            try:
                adj[i].remove(v_idx)
            except Exception as e:
                pass
        self.vertices = self.create_graph(adj)

def toposort(adj, n):
    used = [0] * len(adj)
    order = []
    #write your code here
    directed_graph = Graph(adj, n)
    while directed_graph.vertices != None:
        sink = directed_graph.find_sink()
        if sink != -1:
            order.append(sink)
            print(sink)
            directed_graph.delete_vertex(sink)
        else:
            break
    return order

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    order = toposort(adj, n)
    for x in order:
        print(x + 1, end=' ')

