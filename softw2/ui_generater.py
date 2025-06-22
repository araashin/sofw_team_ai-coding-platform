import base64
import requests
import json

class UIGenerator:
    def __init__(self, vlm_model_name="llava", ollama_api_url="http://localhost:11434/api/generate"):
        self.vlm_model_name = vlm_model_name
        self.ollama_api_url = ollama_api_url

    def _encode_image(self, image_path):
        """Encodes an image to base64 for API transmission."""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
            return None

    def generate_react_code(self, image_path):
        """
        Sends an image of a UI mockup to the local Ollama VLM 
        and receives generated React component code.
        """
        encoded_image = self._encode_image(image_path)
        if not encoded_image:
            return None

        headers = {"Content-Type": "application/json"}
        
        prompt = "This is a UI mockup. Generate a single React component using JSX and Tailwind CSS that implements this design. Only output the code, without any explanation."

        payload = {
            "model": self.vlm_model_name,
            "prompt": prompt,
            "images": [encoded_image],
            "stream": False
        }

        print(f"Sending request to Ollama VLM ({self.vlm_model_name})...")
        try:
            response = requests.post(self.ollama_api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            # VLM 응답에서 코드 블록을 추출하는 것이 더 안정적일 수 있습니다.
            react_code = result.get("response", "").strip()
            if "```" in react_code:
                react_code = react_code.split("```")[1]
                # 'jsx' 나 'javascript' 같은 언어 명시 제거
                if react_code.startswith(('jsx', 'javascript', 'html')):
                    react_code = react_code.split('\n', 1)[1]

            return react_code
            
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama VLM: {e}")
            print("Please ensure Ollama server is running and the 'llava' model is available.")
            return None
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from response: {response.text}")
            return None

if __name__ == "__main__":
    # 이 파일을 직접 실행하여 테스트하려면,
    # 'assets' 폴더를 만들고 그 안에 'mockup.png' 이미지를 넣어주세요.
    ui_gen = UIGenerator()
    mockup_image_path = "assets/mockup.png"
    react_code = ui_gen.generate_react_code(mockup_image_path)

    if react_code:
        print("\n--- Generated React Code ---")
        print(react_code)
        # with open("GeneratedComponent.jsx", "w") as f:
        #     f.write(react_code)
    else:
        print("Failed to generate React code.")