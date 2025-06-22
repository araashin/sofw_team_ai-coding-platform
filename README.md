# LeetCode 문제 수집 및 분석 프로젝트

이 프로젝트는 LeetCode 문제들을 자동으로 수집하고, 설명 및 솔루션을 정리된 폴더 구조로 저장하며, 알고리즘 시각화 기능과 AI 기반 코드 생성 기능까지 포함한 Python 기반 시스템입니다.

## 폴더 구조

```
Project2/
├── main.py                 # 웹 서버 실행 파일 (질문 시스템)
├── add_id_slug.py          # 문제 ID/slug 처리
├── bst.py                  # 이진 탐색 트리 관련 시각화
├── graph.py                # 그래프 시각화 알고리즘
├── requirements.txt        # 필요 패키지 목록
├── backend/
│   ├── LLM.py              # LLM 기반 코드 생성기
│   ├── VLM.py              # VLM (이미지+텍스트) 기반 코드 생성기
├── src/
│   ├── main.py             # LeetCode 문제 수집 파이프라인 실행 파일
│   └── ...                 # 수집, 분석, 시각화 관련 모듈
├── data/
│   ├── problems.json       # 수집된 문제 리스트
│   └── [문제이름]/         # 문제별 설명 및 솔루션 저장 폴더
│       ├── description.html
│       └── solution.py
```

## 주요 기능

- LeetCode 문제 자동 수집 및 구조화 저장  
- 문제 설명(`description.html`)과 솔루션(`solution.py`) 자동 생성  
- LLM/VLM을 활용한 문제 기반 코드 자동 생성  
- 알고리즘 시각화 기능 포함  
- 웹 UI에서 질문/코드 생성을 위한 인터페이스 제공  

## 실행 방법

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. Ollama 서버 실행 (새 터미널에서)

```bash
ollama serve
```

### 3. main.py 실행 (기존 터미널에서)

```bash
python main.py
```

### 4. 안내된 주소에 접속하여 질문 입력 후 사용 가능합니다.

## AI 모듈 설명

- `LLM.py` : 텍스트(문제 설명) 기반 Python 코드 자동 생성
- `VLM.py` : 이미지 + OCR 텍스트 기반 코드 자동 생성

## 수집된 문제 저장 예시

```
data/
├── 3sum/
│   ├── description.html
│   └── solution.py
├── 3sum-closest/
│   ├── description.html
│   └── solution.py
```

## 사용 기술

- ![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
- ![OpenAI](https://img.shields.io/badge/OpenAI-API-black?logo=openai)
- ![Matplotlib](https://img.shields.io/badge/Matplotlib-gray?logo=plotly)
- ![EasyOCR](https://img.shields.io/badge/EasyOCR-gray)
- ![NetworkX](https://img.shields.io/badge/NetworkX-gray)
- ![Requests](https://img.shields.io/badge/Requests-gray)
