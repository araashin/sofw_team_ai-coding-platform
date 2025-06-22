import json

# 원본 problems.json 파일 경로
input_path = "data/problems.json"
# 결과를 저장할 파일 경로
output_path = "data/problems_with_id.json"

with open(input_path, "r", encoding="utf-8") as f:
    problems = json.load(f)

for prob in problems:
    prob["id"] = prob.get("slug") or prob.get("title")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(problems, f, ensure_ascii=False, indent=2)

print(f"변환 완료: {output_path} 파일이 생성되었습니다.")
