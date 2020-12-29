#Uses python3

import sys
import queue

class Heap():
    def __init__(self, data):
        self.array, self.pos = self.create_array(data)
        self.size = len(self.array)
 
    def create_array(self, data):
        arr, pos = [], []
        for i, d in enumerate(data):
            pos.append(i)
            arr.append(d)
        return arr, pos
 
    def swap_node(self, a, b):
        self.array[a], self.array[b] = self.array[b], self.array[a]
 
    def heapify(self, idx): # raise up minimum node
        smallest = idx
        left = 2*idx + 1
        right = 2*idx + 2
        if left < self.size and self.array[left][1] < self.array[smallest][1]:
            smallest = left
        if right < self.size and self.array[right][1] < self.array[smallest][1]:
            smallest = right
        if smallest != idx:
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest
            self.swap_node(smallest, idx)
            self.heapify(smallest)
 
    def extract_min(self):
        if self.is_empty() == True:
            return
        root = self.array[0]
        last_node = self.array[self.size - 1]
        self.array[0] = last_node
        self.pos[last_node[0]] = 0
        self.pos[root[0]] = self.size - 1
        self.size -= 1
        self.heapify(0)
        return root
 
    def is_empty(self):
        return True if self.size == 0 else False
 
    def decrease_key(self, v, dist):
        i = self.pos[v]
        self.array[i][1] = dist
        while i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]:
            self.pos[ self.array[i][0] ] = (i-1)//2
            self.pos[ self.array[(i-1)//2][0] ] = i
            self.swap_node(i, (i - 1)//2 )
            i = (i - 1) // 2;
 
    def in_heap(self, v):
        if self.pos[v] < self.size:
            return True
        return False

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

    def is_negative_cycle(self):
        s = self.vertices[0]
        dist, prev = dict(), dict()
        for u in self.vertices:
            dist[u], prev[u] = sys.maxsize, None
        dist[s] = 0
        flag = False
        found = None
        for i in range(self.n):
            for (u, v) in self.edges:
                f = self.relax(u, v, dist, prev)
                if i == self.n-1:
                    if f:
                        flag = True
                        found = v
        return flag, found, prev

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
    
    def dijkstra(self, s, excluding):
        dist, prev = dict(), dict()
        for u in self.vertices:
            dist[u], prev[u] = sys.maxsize, None
        dist[s] = 0

        heap_l = [[u.key, dist[u]] for u in self.vertices]
        h = Heap(heap_l)        
        h.decrease_key(s.key, dist[s])

        while not h.is_empty():
            u = self.vertices[h.extract_min()[0]]
            if u.key in excluding:
                continue
            for v in u.adj:
                if v == u or u.key in excluding:
                    continue
                v_dist_old = dist[v]
                v_adj_idx = u.adj.index(v)
                tmp = dist[u] + u.cost[v_adj_idx]
                if dist[v] > tmp and dist[u] != sys.maxsize and h.in_heap(v.key):
                    dist[v] = tmp
                    prev[v] = u
                    h.decrease_key(v.key, dist[v])
        return dist

def shortest_paths(adj, cost, s, distance, reachable, shortest):
    #write your code here
    g = Graph(adj, cost)
    flag, v, prev = g.is_negative_cycle()

    # detect negative cycles
    excluding = []
    if flag:
        neg_cycles = g.find_negative_cycle(v, prev)
        for n in neg_cycles:
            excluding.append(n.key)
            shortest[n.key] = 0
            # all nodes reachable by these nodes are negtive too
            for v in n.adj:
                excluding.append(v.key)
                shortest[v.key] = 0

    # if the source does not in negative cycles
    if s not in excluding:
        dist = g.dijkstra(g.vertices[s], excluding)
        for node in dist:
            if node.key not in excluding and dist[node] != sys.maxsize:
                distance[node.key] = dist[node]
                reachable[node.key] = 1
            elif node.key in excluding:
                reachable[node.key] = 1
    else: # the source node itself is in negative cycles
        for node in g.vertices:
            if node.key in excluding:
                reachable[node.key] = 1


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    # n, m = 5,4
    data = data[2:]
    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    # edges = [((1,2),1),((4,1),2), ((2,3),2), ((3,1),-5)]
    data = data[3 * m:]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    s = data[0]
    s -= 1
    # s = 4-1
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
