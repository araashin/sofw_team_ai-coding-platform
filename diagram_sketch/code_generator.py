from typing import List, Dict
from collections import defaultdict, deque

def gen_bst_code(nodes: List[Dict], edges: List[Dict]) -> str:
    lines = [
        "from collections import deque",
        "",
        "class Node:",
        "    def __init__(self, value):",
        "        self.value = value",
        "        self.left = None",
        "        self.right = None",
        "",
        "class BST:",
        "    def __init__(self):",
        "        self.root = None",
        "",
        "    def insert(self, value):",
        "        if not self.root:",
        "            self.root = Node(value)",
        "            return",
        "        curr = self.root",
        "        while True:",
        "            if value < curr.value:",
        "                if curr.left: curr = curr.left",
        "                else: curr.left = Node(value); break",
        "            else:",
        "                if curr.right: curr = curr.right",
        "                else: curr.right = Node(value); break",
        "",
        "    def dfs(self):",
        "        result = []",
        "        def _dfs(node):",
        "            if not node: return",
        "            result.append(node.value)",
        "            _dfs(node.left)",
        "            _dfs(node.right)",
        "        _dfs(self.root)",
        "        return result",
        "",
        "    def bfs(self):",
        "        result = []",
        "        q = deque([self.root])",
        "        while q:",
        "            node = q.popleft()",
        "            if node:",
        "                result.append(node.value)",
        "                q.append(node.left)",
        "                q.append(node.right)",
        "        return result",
        "",
        "def build_bst():",
        "    bst = BST()",
    ]
    for n in nodes:
        lines.append(f"    bst.insert({n['value']})")
    lines += [
        "    return bst",
        "",
        "if __name__ == '__main__':",
        "    bst = build_bst()",
        "    print('DFS:', bst.dfs())",
        "    print('BFS:', bst.bfs())",
    ]
    return "\n".join(lines)


def gen_graph_code(nodes: List[Dict], edges: List[Dict]) -> str:
    lines = [
        "from collections import defaultdict, deque",
        "",
        "class Graph:",
        "    def __init__(self):",
        "        self.adj = defaultdict(list)",
        "",
        "    def add_edge(self, u, v):",
        "        self.adj[u].append(v)",
        "",
        "    def dfs(self, start, visited=None):",
        "        if visited is None: visited = set()",
        "        visited.add(start)",
        "        for nbr in self.adj[start]:",
        "            if nbr not in visited:",
        "                self.dfs(nbr, visited)",
        "        return visited",
        "",
        "    def bfs(self, start):",
        "        visited = set([start])",
        "        q = deque([start])",
        "        while q:",
        "            u = q.popleft()",
        "            for nbr in self.adj[u]:",
        "                if nbr not in visited:",
        "                    visited.add(nbr)",
        "                    q.append(nbr)",
        "        return visited",
        "",
        "def build_graph():",
        "    g = Graph()",
    ]
    for edge in edges:
        if isinstance(edge, dict):
            u = edge['from']
            v = edge['to']
        else:
            u, v = edge
        lines.append(f"    g.add_edge({u}, {v})")
    lines += [
        "    return g",
        "",
        "if __name__ == '__main__':",
        "    g = build_graph()",
        "    start = list(g.adj.keys())[0]",
        "    print('DFS from', start, ':', g.dfs(start))",
        "    print('BFS from', start, ':', g.bfs(start))",
    ]
    return "\n".join(lines)
