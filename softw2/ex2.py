# This is a simplified conceptual implementation for demonstrating the idea.
# A full, robust Red-Black Tree implementation is complex and often uses
# specific libraries or comprehensive textbook algorithms.

class Node:
    RED = True
    BLACK = False

    def __init__(self, key, value, color=RED):
        self.key = key  # Difficulty level
        self.value = value # Problem ID or Problem Object
        self.color = color
        self.left = None
        self.right = None
        self.parent = None # Useful for rotations and deletions

    def __str__(self):
        return f"Node(Key: {self.key}, Color: {'R' if self.color else 'B'})"

class RedBlackTree:
    def __init__(self):
        self.root = None
        # Sentinel node for easier handling of NIL leaves
        self.NIL = Node(None, None, Node.BLACK) # All leaves are NIL and black

    def _is_red(self, node):
        return node is not None and node.color == Node.RED

    def _is_black(self, node):
        return node is None or node.color == Node.BLACK # NIL nodes are black

    # --- Basic BST operations (simplified for concept) ---
    def _insert_bst(self, node, new_node):
        if new_node.key < node.key:
            if node.left is None or node.left == self.NIL:
                node.left = new_node
                new_node.parent = node
            else:
                self._insert_bst(node.left, new_node)
        else: # Allow equal keys, but real RBTs usually handle this precisely
            if node.right is None or node.right == self.NIL:
                node.right = new_node
                new_node.parent = node
            else:
                self._insert_bst(node.right, new_node)

    def insert(self, key, value):
        new_node = Node(key, value)
        if self.root is None:
            self.root = new_node
            self.root.color = Node.BLACK # Root is always black
        else:
            self._insert_bst(self.root, new_node)
            # After insertion, you would call a fix-up function to maintain RBT properties
            # self._fix_insert(new_node) # This is the complex part of RBT
            print(f"Inserted problem with difficulty {key}. (Requires RBT fix-up logic for balancing)")


    def search(self, key):
        """Searches for a node with the given key (difficulty)."""
        current = self.root
        while current and current != self.NIL:
            if key == current.key:
                return current.value
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None # Key not found

    def get_problems_at_or_around_difficulty(self, target_difficulty, range_offset=1):
        """
        Finds problems at or around the target difficulty.
        In a real scenario, this would involve a more sophisticated
        traversal to collect nodes within a range.
        """
        problems = []
        # For simplicity, let's just do an in-order traversal and collect matching ones
        # A more efficient way would be a range query in a true RBT.
        nodes_to_visit = [self.root]
        while nodes_to_visit:
            node = nodes_to_visit.pop(0) # BFS-like for simplicity, can be DFS
            if node and node != self.NIL:
                if (target_difficulty - range_offset) <= node.key <= (target_difficulty + range_offset):
                    problems.append(node.value)
                if node.left and node.left != self.NIL:
                    nodes_to_visit.append(node.left)
                if node.right and node.right != self.NIL:
                    nodes_to_visit.append(node.right)
        return problems

    # --- Red-Black Tree Specific Operations (Stubs for complexity) ---
    # These functions are the core of Red-Black Tree self-balancing.
    # Implementing them accurately is non-trivial and involves
    # left_rotate, right_rotate, and color changes based on 6-7 cases for insertion,
    # and even more for deletion.
    def _left_rotate(self, node):
        # Implementation of left rotation
        pass

    def _right_rotate(self, node):
        # Implementation of right rotation
        pass

    def _fix_insert(self, new_node):
        # Implementation of the complex insertion fix-up logic
        # Involves checking parent, grandparent, uncle colors, and performing rotations/recoloring
        pass

    def _fix_delete(self, node):
        # Implementation of the even more complex deletion fix-up logic
        pass

    # --- For visualization/testing (optional) ---
    def inorder_traversal(self):
        """Returns keys in sorted order."""
        result = []
        def _traverse(node):
            if node and node != self.NIL:
                _traverse(node.left)
                result.append(node.key)
                _traverse(node.right)
        _traverse(self.root)
        return result

# Example Usage:
if __name__ == "__main__":
    difficulty_manager = RedBlackTree()

    # Add some problems with their difficulties
    # In a real app, 'problem_id_X' would be a dictionary or object
    # representing the full problem (title, description, solution, etc.)
    difficulty_manager.insert(5, {"id": "p001", "title": "Easy Array Sum"})
    difficulty_manager.insert(10, {"id": "p002", "title": "Medium String Reversal"})
    difficulty_manager.insert(3, {"id": "p003", "title": "Beginner Hello World"})
    difficulty_manager.insert(15, {"id": "p004", "title": "Hard Graph Traversal"})
    difficulty_manager.insert(7, {"id": "p005", "title": "Medium-Easy Palindrome Check"})
    difficulty_manager.insert(12, {"id": "p006", "title": "Medium-Hard Dynamic Programming"})

    print("\nProblems (conceptually inserted, RBT balancing not fully shown):")
    print(difficulty_manager.inorder_traversal())

    # Simulate user progress
    user_skill_level = 8 # User is currently good at difficulty 8 problems

    print(f"\nUser skill level: {user_skill_level}")
    recommended_problems = difficulty_manager.get_problems_at_or_around_difficulty(user_skill_level, range_offset=2)

    if recommended_problems:
        print(f"Recommended problems for difficulty around {user_skill_level}:")
        for problem in recommended_problems:
            print(f"- {problem['title']} (ID: {problem['id']})")
    else:
        print("No problems found around the user's current difficulty.")

    # Another scenario
    user_skill_level = 4
    print(f"\nUser skill level: {user_skill_level}")
    recommended_problems = difficulty_manager.get_problems_at_or_around_difficulty(user_skill_level, range_offset=1)
    if recommended_problems:
        print(f"Recommended problems for difficulty around {user_skill_level}:")
        for problem in recommended_problems:
            print(f"- {problem['title']} (ID: {problem['id']})")