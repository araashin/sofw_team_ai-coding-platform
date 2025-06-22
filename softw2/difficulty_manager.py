# Example using sortedcontainers for difficulty management
from sortedcontainers import SortedDict

class SimplifiedDifficultyManager:
    def __init__(self):
        self.problems_by_difficulty = SortedDict() # Key: difficulty, Value: list of problems

    def add_problem(self, difficulty, problem_data):
        if difficulty not in self.problems_by_difficulty:
            self.problems_by_difficulty[difficulty] = []
        self.problems_by_difficulty[difficulty].append(problem_data)
        print(f"Added problem: {problem_data['title']} (Difficulty: {difficulty})")

    def get_problems_at_or_around_difficulty(self, target_difficulty, range_offset=1):
        recommended = []
        for diff in self.problems_by_difficulty.keys():
            if (target_difficulty - range_offset) <= diff <= (target_difficulty + range_offset):
                recommended.extend(self.problems_by_difficulty[diff])
        return recommended

if __name__ == "__main__":
    sd_manager = SimplifiedDifficultyManager()
    sd_manager.add_problem(5, {"id": "p001", "title": "Easy Array Sum"})
    sd_manager.add_problem(10, {"id": "p002", "title": "Medium String Reversal"})
    sd_manager.add_problem(3, {"id": "p003", "title": "Beginner Hello World"})
    sd_manager.add_problem(15, {"id": "p004", "title": "Hard Graph Traversal"})
    sd_manager.add_problem(7, {"id": "p005", "title": "Medium-Easy Palindrome Check"})
    sd_manager.add_problem(12, {"id": "p006", "title": "Medium-Hard Dynamic Programming"})

    user_skill = 8
    print(f"\nUser skill level: {user_skill}")
    recs = sd_manager.get_problems_at_or_around_difficulty(user_skill, range_offset=2)
    if recs:
        print("Recommended problems:")
        for p in recs:
            print(f"- {p['title']} (ID: {p['id']})")