import requests
import json
import base64
import os

def get_vlm_response(image_path, prompt):
    if not os.path.exists(image_path):
        return "이미지 파일을 찾을 수 없습니다."

    try:
        with open(image_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode("utf-8")

        prompt = f"다음 그림을 한국어로 설명해줘:\n\n{prompt}" # 한글 지시 

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llava",
                "prompt": prompt,
                "images": [encoded_image]
            },
            stream=True
        )

        # 응답
        full_response = ""
        for chunk in response.iter_lines():
            if chunk:
                data = chunk.decode("utf-8")
                if '"response":"' in data:
                    json_data = json.loads(data)
                    full_response += json_data.get("response", "")

        return full_response.strip().replace("\\n", "\n") or "VLM 응답이 비어 있습니다."

    except Exception as e:
        return f"오류 발생: {e}"
    