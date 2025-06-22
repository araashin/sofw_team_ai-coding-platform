import requests
import json

class OllamaLLM:
    def __init__(self, model_name="llama2", ollama_api_url="http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.ollama_api_url = ollama_api_url

    def generate_response(self, prompt, system_message=None, temperature=0.7):
        """
        Ollama LLM에 프롬프트를 보내고 응답을 받습니다.
        """
        headers = {"Content-Type": "application/json"}
        
        # 메시지 구성
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        # API 요청 바디
        data = {
            "model": self.model_name,
            "prompt": prompt, # legacy /generate endpoint uses 'prompt' not 'messages'
            "stream": False,  # 스트리밍 응답을 받을 것인지 여부 (True면 generator 반환)
            "options": {
                "temperature": temperature
            }
        }
        # Note: Ollama's /api/generate endpoint still primarily uses the 'prompt' field for simple text generation.
        # For chat-like interactions with 'role' messages, the /api/chat endpoint is more appropriate.
        # However, for basic prompt-response, /api/generate with 'prompt' works fine.
        # If you want to use the /api/chat endpoint, the data structure would change to include 'messages':
        # data = {
        #     "model": self.model_name,
        #     "messages": messages,
        #     "stream": False,
        #     "options": {
        #         "temperature": temperature
        #     }
        # }
        # And the ollama_api_url would be "http://localhost:11434/api/chat"

        print(f"Sending request to Ollama ({self.model_name})...")
        try:
            response = requests.post(self.ollama_api_url, headers=headers, data=json.dumps(data))
            response.raise_for_status() # HTTP 오류가 발생하면 예외 발생

            result = response.json()
            return result.get("response") # /generate endpoint의 응답 필드
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            print("Please ensure Ollama server is running (e.g., by running 'ollama run llama2' in a terminal).")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON response from Ollama: {response.text}")
            return None

# 예시 사용법:
if __name__ == "__main__":
    # Ollama 서버가 실행 중이어야 합니다 (터미널에서 'ollama run llama2' 실행).
    ollama_llm = OllamaLLM(model_name="llama2")

    # 1. 간단한 질문
    prompt1 = "What is the capital of France?"
    response1 = ollama_llm.generate_response(prompt1)
    if response1:
        print(f"\nPrompt: {prompt1}")
        print(f"Response: {response1}")

    # 2. 시스템 메시지와 함께 (만약 /api/chat 엔드포인트를 사용한다면 유용)
    # 현재 /api/generate는 system_message를 직접 지원하지 않지만,
    # prompt에 system_message를 포함시키는 방식으로 우회할 수 있습니다.
    prompt2 = "As a helpful coding assistant, explain how to declare a variable in Python."
    response2 = ollama_llm.generate_response(prompt2)
    if response2:
        print(f"\nPrompt: {prompt2}")
        print(f"Response: {response2}")

    # 3. 다른 모델 사용 (만약 다른 모델을 다운로드했다면)
    # ollama_llm_codellama = OllamaLLM(model_name="codellama")
    # code_prompt = "Write a Python function to calculate the factorial of a number."
    # code_response = ollama_llm_codellama.generate_response(code_prompt)
    # if code_response:
    #     print(f"\nPrompt: {code_prompt}")
    #     print(f"Response: {code_response}")