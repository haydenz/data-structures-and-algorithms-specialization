#Uses python3

import sys
import queue
import math

class Vertex:
    def __init__(self, key):
        self.key = key
        self.adj = []
        self.cost = []
        self.visited = False

class Graph:
    def __init__(self, adj, cost):
        self.adj = adj
        self.n = len(adj)
        self.cost = cost
        self.vertices = []
        self.create_vertices()
        self.edges = self.edges()
    
    def create_vertices(self):
        vertices = [None for _ in range(self.n)]
        for i in range(self.n):
            vertices[i] = Vertex(i)
        for i in range(self.n):
            vertices[i].cost = self.cost[i]
            for a in adj[i]:
                vertices[i].adj.append(vertices[a])
        self.vertices = vertices
    
    def edges(self):
        res = []
        for u in self.vertices:
            for v in u.adj:
                res.append((u, v))
        return res

    def is_negative_cycle(self, s):
        dist, prev = dict(), dict()
        for u in self.vertices:
            dist[u], prev[u] = math.inf, None
        dist[s] = 0
        flag = False
        found = []
        for i in range(self.n):
            for (u, v) in self.edges:
                f = self.relax(u, v, dist, prev)
                if i == self.n-1:
                    if f:
                        flag = True
                        found.append(v)
        return flag, found, prev, dist

    def relax(self, u, v, dist, prev):
        flag = False
        v_adj_idx = u.adj.index(v)
        tmp = dist[u] + u.cost[v_adj_idx]
        if dist[v] > tmp:
            dist[v] = tmp
            prev[v] = u
            flag = True
        del tmp
        return flag
    
    def find_negative_cycle(self, v, prev):
        x = v
        for _ in range(self.n):
            x = prev[x]

        y = x
        res = [x]
        x = prev[x]
        while x != y:
            res.append(x)
            x = prev[x]
        
        return res


def shortest_paths(adj, cost, s, distance, reachable, shortest):
    #write your code here
    g = Graph(adj, cost)
    source = g.vertices[s]
    flag, found, prev, dist = g.is_negative_cycle(source)

    # calculate distance
    # dist = g.dijkstra(source)
    for node in dist:
        if dist[node] != math.inf:
            reachable[node.key] = 1
            distance[node.key] = dist[node]

    # detect negative cycles
    neg = []
    if flag:
        for v in found:
            neg_cycles = g.find_negative_cycle(v, prev)
            neg += neg_cycles
    neg = list(set(neg))

    # BFS
    q = queue.Queue(maxsize=g.n)
    for n in neg:
        q.put(n)
        n.visited = True
    while not q.empty():
        u = q.get()
        for v in u.adj:
            if not v.visited:
                q.put(v)
                neg.append(v)
            else:
                continue

    for n in neg:
        if dist[n] != math.inf:
            reachable[n.key] = 1
            shortest[n.key] = 0


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    # n, m = 6,7
    data = data[2:]
    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    # edges = [((5,6),7),((6,5),-9), ((1,3),1), ((3,2),-8),((2,4),3),((4,3),2),((1,5),2)]
    data = data[3 * m:]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    s = data[0]
    s -= 1
    # s = 1-1
    distance = [10**19] * n
    reachable = [0] * n
    shortest = [1] * n
    shortest_paths(adj, cost, s, distance, reachable, shortest)
    for x in range(n):
        if reachable[x] == 0:
            print('*')
        elif shortest[x] == 0:
            print('-')
        else:
            print(distance[x])
