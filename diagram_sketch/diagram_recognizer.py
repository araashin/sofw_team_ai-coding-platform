from diagram_sketch.ocr.ocr_helper import extract_numbers_easyocr

def recognize(image_path: str) -> dict:
    numbers = extract_numbers_easyocr(image_path)
    if not numbers or len(numbers) < 2:
        return {
            "type": "graph",
            "nodes": [{"value": n} for n in numbers],
            "edges": [],
            "confidence": 1.0,
        }
    edges = [{"from": numbers[i], "to": numbers[i+1]} for i in range(len(numbers)-1)]
    return {
        "type": "graph",
        "nodes": [{"value": n} for n in numbers],
        "edges": edges,
        "confidence": 1.0,
    }

def parse_structure(vlm_output: dict) -> tuple:
    nodes = vlm_output.get('nodes', [])
    edges = vlm_output.get('edges', [])
    return nodes, edges
