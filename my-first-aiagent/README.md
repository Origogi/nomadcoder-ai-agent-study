# My First AI Agent

OpenAI의 Function Calling 기능을 사용한 AI 에이전트 예제 프로젝트입니다.

## 📚 학습 출처

이 프로젝트는 노마드 코더의 **AI Agents Masterclass** 강의를 통해 학습하며 작성되었습니다.

🎓 강의 링크: [AI Agents Masterclass](https://nomadcoders.co/ai-agents-masterclass/lobby)

## 📖 프로젝트 소개

OpenAI의 Function Calling API를 사용하여 AI가 특정 함수를 호출할 수 있도록 구현한 대화형 에이전트입니다.

### 주요 기능

- ✅ OpenAI GPT-4o-mini 모델 사용
- ✅ Function Calling을 통한 Tool 실행
- ✅ 대화 히스토리 메모라이제이션
- ✅ Jupyter 노트북 기반 인터랙티브 개발 환경

## 🛠️ 기술 스택

- **Python**: 3.13+
- **OpenAI API**: GPT-4o-mini
- **패키지 관리**: uv
- **개발 환경**: Jupyter Notebook

## 📋 요구사항

- Python 3.13 이상
- OpenAI API 키
- uv 패키지 매니저

## 🚀 설치 및 실행

### 1. 레포지토리 클론

```bash
git clone https://github.com/Origogi/my-first-aiagent.git
cd my-first-aiagent
```

### 2. 의존성 설치

```bash
uv sync
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 OpenAI API 키를 추가하세요:

```bash
OPENAI_API_KEY="your-api-key-here"
```

### 4. Jupyter 노트북 실행

VS Code에서 `main.ipynb` 파일을 열고 셀을 순서대로 실행합니다.

## 📁 프로젝트 구조

```
.
├── main.ipynb          # 메인 Jupyter 노트북 (Function Calling 구현)
├── main.py             # Python 스크립트 진입점
├── pyproject.toml      # 프로젝트 설정 및 의존성
├── CLAUDE.md           # 프로젝트 가이드 (Claude Code용)
└── .env                # 환경 변수 (git에서 제외됨)
```

## 🔧 주요 컴포넌트

### 1. Tool 함수 정의
AI가 호출할 수 있는 함수들을 정의합니다.

```python
def get_weather(city):
    """특정 도시의 날씨 정보를 반환합니다."""
    return f"The weather in {city} is sunny with a high of 100°C."
```

### 2. Tool 스키마 정의
OpenAI API에 전달할 Tool 정보를 JSON 형식으로 정의합니다.

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather information for a given city.",
            "parameters": { ... }
        }
    }
]
```

### 3. Function Mapping
함수 이름과 실제 함수를 매핑합니다.

```python
FUNCTION_MAPPINGS = {
    "get_weather": get_weather
}
```

### 4. AI 응답 처리
AI의 응답에서 tool_calls를 확인하고 함수를 실행합니다.

## 💡 사용 예시

```
User: 서울 날씨 알려줘
AI: [get_weather 함수 호출]
AI: 서울의 날씨는 맑고 최고 기온은 100°C입니다.
```

## 📝 학습 내용

- OpenAI Function Calling API 사용법
- Tool 정의 및 매핑 패턴
- 대화 히스토리 관리
- 재귀적 AI 호출 패턴
- Python dotenv를 사용한 환경 변수 관리

## 🔐 보안

- `.env` 파일은 `.gitignore`에 포함되어 있어 GitHub에 업로드되지 않습니다.
- API 키는 절대 커밋하지 마세요.

## 📚 참고 자료

- [OpenAI Function Calling 공식 문서](https://platform.openai.com/docs/guides/function-calling)
- [노마드 코더 - AI Agents Masterclass](https://nomadcoders.co/ai-agents-masterclass/lobby)

## 👤 작성자

김정태 ([@Origogi](https://github.com/Origogi))

## 📄 라이선스

이 프로젝트는 학습 목적으로 작성되었습니다.
