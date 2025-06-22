from collections import defaultdict, deque

class Graph:
    def __init__(self):
        self.adj = defaultdict(list)

    def add_edge(self, u, v):
        self.adj[u].append(v)

    def dfs(self, start, visited=None):
        if visited is None: visited = set()
        visited.add(start)
        for nbr in self.adj[start]:
            if nbr not in visited:
                self.dfs(nbr, visited)
        return visited

    def bfs(self, start):
        visited = set([start])
        q = deque([start])
        while q:
            u = q.popleft()
            for nbr in self.adj[u]:
                if nbr not in visited:
                    visited.add(nbr)
                    q.append(nbr)
        return visited

def build_graph():
    g = Graph()
    g.add_edge(82, 7)
    g.add_edge(7, 5)
    g.add_edge(5, 3)
    g.add_edge(3, 5)
    g.add_edge(5, 5)
    g.add_edge(5, 5)
    g.add_edge(5, 5)
    g.add_edge(5, 5)
    g.add_edge(5, 22)
    g.add_edge(22, 22)
    g.add_edge(22, 7)
    return g

if __name__ == '__main__':
    g = build_graph()
    start = list(g.adj.keys())[0]
    print('DFS from', start, ':', g.dfs(start))
    print('BFS from', start, ':', g.bfs(start))