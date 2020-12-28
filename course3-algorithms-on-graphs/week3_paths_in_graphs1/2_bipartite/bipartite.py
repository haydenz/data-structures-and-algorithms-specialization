#Uses python3

import sys
import queue


class Vertex:
    def __init__(self, key):
        self.key = key
        self.adj = []
        self.visited = False

class Graph:
    def __init__(self, adj, n):
        self.adj = adj
        self.n = n
        self.vertices = []
        self.create_vertices()
    
    def create_vertices(self):
        vertices = [None for _ in range(self.n)]
        for i in range(self.n):
            vertices[i] = Vertex(i)
        for i in range(self.n):
            for a in adj[i]:
                vertices[i].adj.append(vertices[a])
        self.vertices = vertices
    
    def BFS(self, s):
        color, dist, flag = dict(), dict(), dict()
        for u in self.vertices:
            color[u] = None
            dist[u] = -1
            flag[u] = True
        color[s] = 0
        dist[s] = 0
        q = queue.Queue(maxsize=n)
        q.put(s)
        while not q.empty():
            u = q.get()
            for v in u.adj:
                if dist[v] == -1:
                    q.put(v)
                    dist[v] = dist[u] + 1
                if color[v] == None:
                    color[v] = 1 if color[u] == 0 else 0
                elif color[v] == color[u]:
                    flag[v] = False
                else:
                    pass
        return dist, flag

def bipartite(adj, n):
    #write your code here
    graph = Graph(adj, n)
    verteices = graph.vertices
    v = verteices[0]
    dist, flag = graph.BFS(v)

    while -1 in dist.values():
        contradictions = [f for f in flag.values() if f != None]
        if not all(contradictions):
            return 0
        v = list(dist.keys())[list(dist.values()).index(-1)]
        uncheck = [i for i,_ in enumerate(list(dist.values())) if _ == -1]
        graph.vertices = [graph.vertices[i] for i in uncheck]
        graph.n = len(graph.vertices)
        dist, flag = graph.BFS(v)

    contradictions = [f for f in flag.values() if f != None]
    if not all(contradictions):
        return 0
    return 1

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    # n,m= 4,2
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    # edges = [(1,2),(3,4)]
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(bipartite(adj, n))
