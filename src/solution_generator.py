import os
import re
from typing import List, Dict

def safe_dirname(name: str) -> str:
    name = name.strip().replace(" ", "_")
    return re.sub(r"[^a-zA-Z0-9_]", "", name)

def generate_solution_stubs(problems: List[Dict], dir_path: str = 'solutions'):
    print(f"[LOG] generate_solution_stubs called, 문제 수: {len(problems)}")
    os.makedirs(dir_path, exist_ok=True)
    mapping = {1: 'Easy', 2: 'Medium', 3: 'Hard'}
    for p in problems:
        slug = p['slug']
        diff = mapping.get(p['difficulty'], 'Unknown')
        title = p.get('title', 'Unknown')
        url = p.get('url', 'Unknown')
        subdir = os.path.join(dir_path, safe_dirname(title))
        os.makedirs(subdir, exist_ok=True)
        filename = os.path.join(subdir, slug + '.py')
        header = '''"""
[{diff}] {title}
URL: {url}
"""

class Solution:
    def solve(self, *args, **kwargs):
        pass
'''.format(diff=diff, title=title, url=url)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header)
    print(f"[LOG] solutions 폴더 최종 파일 개수: {sum([len(files) for _, _, files in os.walk(dir_path)])}")
