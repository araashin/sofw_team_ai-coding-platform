import os
import sys
import cv2
import easyocr
from flask import Flask, render_template, request

from backend.LLM import get_llm_response
from backend.VLM import get_vlm_response

from diagram_sketch.image_processor import preprocess, save_temp
from diagram_sketch.diagram_recognizer import recognize, parse_structure
from diagram_sketch.code_generator import gen_bst_code, gen_graph_code
from diagram_sketch.ocr.ocr_helper import extract_numbers_easyocr

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

BLUR_THRESH = 149
CONF_THRESH = 0.8
ocr_reader = easyocr.Reader(['en'], gpu=False)

def blur_score(path: str) -> float:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return cv2.Laplacian(img, cv2.CV_64F).var()

def detect_label(image_path: str) -> str:
    labels = ocr_reader.readtext(image_path, detail=0)
    for text in labels:
        txt = text.strip().lower()
        if 'graph' in txt:
            return 'graph'
        if 'bst' in txt:
            return 'bst'
    return None

def run_diagram_pipeline(image_path: str):
    explicit = detect_label(image_path)
    numbers = extract_numbers_easyocr(image_path)
    needs_pre = blur_score(image_path) <= BLUR_THRESH

    try:
        vlm_out = recognize(image_path)
        nodes, edges = parse_structure(vlm_out)
        if needs_pre or not nodes or not edges or vlm_out.get("confidence", 0) <= CONF_THRESH:
            raise ValueError
    except Exception:
        img = preprocess(image_path)
        temp_path = "temp.png"
        save_temp(img, temp_path)
        vlm_out = recognize(temp_path)
        nodes, edges = parse_structure(vlm_out)

    if explicit:
        vlm_out['type'] = explicit
    if vlm_out.get("type") == "bst" and numbers:
        nodes = [{"value": n} for n in numbers]
        edges = []

    print(f"Type: {vlm_out.get('type')}, Nodes:{len(nodes)}, Edges:{len(edges)}, Conf:{vlm_out.get('confidence',0):.2f}")

    if vlm_out.get("type") == "bst":
        code = gen_bst_code(nodes, edges)
        out_file = "bst.py"
    else:
        code = gen_graph_code(nodes, edges)
        out_file = "graph.py"

    with open(out_file, "w") as f:
        f.write(code)
    print(f"Generated code saved to {out_file}")
    return out_file

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    question = request.form.get("question")
    image_file = request.files.get("image")

    if image_file and image_file.filename:
        image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)
        code_path = run_diagram_pipeline(image_path)
        with open(code_path, 'r') as f:
            answer = f.read()
    else:
        answer = get_llm_response(question)

    return answer


import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
SOLUTIONS_DIR = os.path.join(PROJECT_ROOT, "solutions")

with open(os.path.join(DATA_DIR, "problems.json"), encoding="utf-8") as f:
    problems_data = json.load(f)

@app.route("/problems", methods=["GET"])
def get_problems():
    return {
        "problems": [
            {
                "id": p["id"],
                "title": p.get("title", ""),
                "name": p.get("name", ""),
                "difficulty": p.get("difficulty", "")
            } for p in problems_data
        ]
    }

@app.route("/problem/<pid>", methods=["GET"])
def get_problem(pid):
    prob = next((p for p in problems_data if str(p["id"]) == pid), None)
    if not prob:
        return {"error": "Problem not found"}, 404
    return prob

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    user_code = data.get('code', '')
    pid = data.get('pid', None)
    prob = next((p for p in problems_data if p["id"] == pid), None)
    if not prob:
        return {"error": "Problem not found"}, 404
    solution_dir = os.path.join(SOLUTIONS_DIR, prob["title"].replace(" ", "_"))
    solution_code = ""
    if os.path.isdir(solution_dir):
        for file in os.listdir(solution_dir):
            if file.endswith(".py"):
                with open(os.path.join(solution_dir, file), encoding="utf-8") as f:
                    solution_code = f.read()
                break
    is_correct = "pass" not in user_code
    review = get_llm_response(user_code) if user_code else "AI 코드리뷰 예시"
    return {
        "is_correct": is_correct,
        "model_answer": solution_code,
        "review": review
    }

if __name__ == "__main__":
    if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
        run_diagram_pipeline(sys.argv[1])
    else:
        app.run(debug=True)

