# Finance Advisor Agent

Google ADK(Agent Development Kit)와 Firecrawl을 활용하여 실시간 금융 데이터를 분석하고 통찰력을 제공하는 AI 에이전트 프로젝트입니다.

## 🚀 프로젝트 개요

이 프로젝트는 최신 AI 기술을 활용하여 금융 시장의 뉴스와 트렌드를 수집하고 분석합니다.
- **Firecrawl**을 사용하여 실시간 웹 검색 및 데이터 스크래핑을 수행합니다.
- **Google ADK** 프레임워크를 기반으로 확장 가능한 에이전트 워크플로우를 구축했습니다.

## 🛠 기술 스택

- **Language**: Python 3.13+
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (빠르고 효율적인 Python 패키지 관리자)
- **Framework**: google-adk
- **Tools**: Firecrawl, Python-dotenv

## ⚙️ 환경 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 키를 설정해야 합니다:

```env
OPENAI_API_KEY=your_openai_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
GOOGLE_API_KEY=your_google_api_key_here  # 선택 사항 (Gemini 사용 시)
```

## 📦 설치 및 실행

이 프로젝트는 `uv`를 사용하여 의존성을 관리합니다.

### 1. 의존성 설치
```bash
uv sync
```

### 2. 에이전트 실행 (Web Interface)
```bash
uv run adk web
```
또는 포그라운드 실행:
```bash
uv run python -m google.adk.cli web
```

## 📝 커밋 가이드

이 프로젝트는 [Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따릅니다.
자세한 내용은 `gemini.md`를 참고하세요.

- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포맷팅
- `refactor`: 리팩토링
