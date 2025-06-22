import os
import re
import json
import requests
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

DIFFICULTY_MAP = {
    "Easy": 1,
    "Medium": 2,
    "Hard": 3
}

def safe_slug(slug: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', slug)

def extract_input_example(description_html: str) -> str:
    from html import unescape
    pre_blocks = re.findall(r'<pre>(.*?)</pre>', description_html, re.DOTALL)
    for block in pre_blocks:
        lines = block.split('\n')
        for line in lines:
            line = unescape(line)
            m = re.match(r'^(?:<strong>)?Input:(?:</strong>)?\s*(.*)', line)
            if m:
                return m.group(1).strip()
    m2 = re.search(r'Input:.*?=\s*([\[\{][\s\S]*?[\]\}])', description_html)
    if m2:
        return m2.group(1)
    return None


def fetch_problem_list(limit: int = 100) -> List[Dict]:
    print(f"[LOG] 상위 {limit}개 문제 수집 중 (GraphQL)")
    graphql_url = "https://leetcode.com/graphql"
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
        problemsetQuestionList: questionList(
        categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
        ) {
            totalNum
            data {
                title
                titleSlug
                difficulty
            }
        }
    }
    """
    payload = {
        "operationName": "problemsetQuestionList",
        "variables": {
            "categorySlug": "",
            "skip": 0,
            "limit": limit,
            "filters": {}
        },
        "query": query
    }
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com/problemset/all/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        res = requests.post(graphql_url, json=payload, headers=headers)
        if res.status_code != 200:
            print(f"[ERROR] 응답 코드: {res.status_code}")
            print(f"[ERROR] 본문:\n{res.text}")
            raise Exception("문제 리스트 요청 실패")
        node = res.json()["data"]["problemsetQuestionList"]
        questions = node.get("data", [])
        print(f"[LOG] 실제 GraphQL로 받은 문제 수: {len(questions)}")
        return [
            {
                "title": q["title"],
                "slug": q["titleSlug"],
                "difficulty": DIFFICULTY_MAP.get(q["difficulty"], 0),
                "url": f"https://leetcode.com/problems/{q['titleSlug']}/"
            }
            for q in questions
        ]
    except Exception as e:
        print(f"[ERROR] fetch_problem_list 실패: {e}")
        return []

def fetch_problem_detail(slug: str) -> Dict[str, str]:
    graphql_url = "https://leetcode.com/graphql"
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            content
            codeSnippets {
                lang
                langSlug
                code
            }
        }
    }
    """
    payload = {
        "operationName": "questionData",
        "variables": {"titleSlug": slug},
        "query": query
    }
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/problems/{slug}/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        res = requests.post(graphql_url, json=payload, headers=headers)
        if res.status_code != 200:
            raise Exception(f"{slug} 요청 실패: {res.status_code}")
        q = res.json()["data"]["question"]
        content = q.get("content") or "<p>문제 설명 없음</p>"
        code = "# 코드 없음"
        for snippet in q.get("codeSnippets", []):
            if snippet.get("langSlug") == "python3":
                code = snippet.get("code", code)
                break
        input_example = extract_input_example(content)
        return {"description": content, "solution": code, "input_example": input_example}
    except Exception as e:
        print(f"[ERROR] {slug} 문제 상세 정보 수집 실패: {e}")
        return {"description": "<p>로딩 실패</p>", "solution": "# 코드 없음", "input_example": None}

def fetch_problems(limit: int = 100) -> List[Dict]:
    problems = fetch_problem_list(limit)
    if not problems:
        print("[ERROR] LeetCode 문제 리스트 수집에 실패했습니다. 결과가 비어 있습니다.")
        return []

    os.makedirs("data", exist_ok=True)
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_slug = {executor.submit(fetch_problem_detail, p["slug"]): p for p in problems}
        for future in as_completed(future_to_slug):
            p = future_to_slug[future]
            slug = p["slug"]
            try:
                detail = future.result()
            except Exception as e:
                print(f"[ERROR] {slug} 수집 실패: {e}")
                detail = {"description": "<p>로딩 실패</p>", "solution": "# 코드 없음", "input_example": None}
            p.update(detail)
            results.append(p)

            folder = os.path.join("data", safe_slug(slug))
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, "description.html"), "w", encoding="utf-8") as f:
                f.write(detail["description"])
            with open(os.path.join(folder, "solution.py"), "w", encoding="utf-8") as f:
                f.write(detail["solution"])

    with open("data/problems.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[LOG] fetch_problems: 최종 수집된 문제 수: {len(results)}")
    return results

if __name__ == "__main__":
    fetch_problems(limit=100)
