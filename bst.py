from collections import deque

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
            return
        curr = self.root
        while True:
            if value < curr.value:
                if curr.left: curr = curr.left
                else: curr.left = Node(value); break
            else:
                if curr.right: curr = curr.right
                else: curr.right = Node(value); break

    def dfs(self):
        result = []
        def _dfs(node):
            if not node: return
            result.append(node.value)
            _dfs(node.left)
            _dfs(node.right)
        _dfs(self.root)
        return result

    def bfs(self):
        result = []
        q = deque([self.root])
        while q:
            node = q.popleft()
            if node:
                result.append(node.value)
                q.append(node.left)
                q.append(node.right)
        return result

def build_bst():
    bst = BST()
    bst.insert(1)
    bst.insert(2)
    bst.insert(7)
    bst.insert(8)
    bst.insert(3)
    bst.insert(6)
    bst.insert(9)
    bst.insert(12)
    bst.insert(4)
    bst.insert(5)
    bst.insert(10)
    bst.insert(11)
    return bst

if __name__ == '__main__':
    bst = build_bst()
    print('DFS:', bst.dfs())
    print('BFS:', bst.bfs())