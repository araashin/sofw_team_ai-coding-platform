import requests
import json

def get_llm_response(prompt):
    try:
        prompt = f"다음 질문에 대해 한국어로 답변해줘:\n\n{prompt}" # 한글 지시 

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", 
                  "prompt": prompt
                  },
            stream=True
        )

        #응답
        full_response = ""
        for chunk in response.iter_lines():
            if chunk:
                data = chunk.decode("utf-8")
                if '"response":"' in data:
                    json_data = json.loads(data)
                    full_response += json_data.get("response", "")

        return full_response.strip() or "LLM 응답이 비어 있습니다."

    except Exception as e:
        return f"오류 발생: {e}"

