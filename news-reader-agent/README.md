# News Reader Agent

CrewAI와 OpenAI를 사용한 뉴스 읽기 및 요약 AI 에이전트입니다.

## 📚 학습 출처

이 프로젝트는 노마드 코더의 **AI Agents Masterclass** 강의를 통해 학습하며 작성되었습니다.

🎓 강의 링크: [AI Agents Masterclass](https://nomadcoders.co/ai-agents-masterclass/lobby)

## 📖 프로젝트 소개

CrewAI 프레임워크를 활용하여 뉴스를 자동으로 수집하고 요약하는 AI 에이전트 시스템입니다.

### 주요 기능

- ✅ CrewAI 기반 멀티 에이전트 시스템
- ✅ 뉴스 검색 및 스크래핑
- ✅ 자동 뉴스 요약
- ✅ OpenAI GPT 모델 활용
- ✅ Jupyter 노트북 기반 인터랙티브 개발 환경

## 🛠️ 기술 스택

- **Python**: 3.13+
- **CrewAI**: 멀티 에이전트 오케스트레이션
- **OpenAI API**: GPT 모델
- **패키지 관리**: uv
- **개발 환경**: Jupyter Notebook

## 📋 요구사항

- Python 3.13 이상
- OpenAI API 키
- uv 패키지 매니저

## 🚀 설치 및 실행

### 1. 레포지토리 클론

```bash
git clone https://github.com/Origogi/news-reader-agent.git
cd news-reader-agent
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
├── main.ipynb          # 메인 Jupyter 노트북 (CrewAI 구현)
├── main.py             # Python 스크립트 진입점
├── pyproject.toml      # 프로젝트 설정 및 의존성
├── CLAUDE.md           # 프로젝트 가이드 (Claude Code용)
└── .env                # 환경 변수 (git에서 제외됨)
```

## 🤖 CrewAI 아키텍처

### Agents
- **News Researcher**: 뉴스 검색 및 수집
- **Content Analyzer**: 뉴스 분석 및 요약
- **Report Writer**: 최종 리포트 작성

### Tools
- **SerperDevTool**: 뉴스 검색
- **ScrapeWebsiteTool**: 웹사이트 스크래핑
- **PDFSearchTool**: PDF 문서 검색

## 💡 사용 예시

```python
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# 에이전트 생성
news_agent = Agent(
    role='News Researcher',
    goal='Find and summarize the latest tech news',
    tools=[SerperDevTool(), ScrapeWebsiteTool()]
)

# 크루 실행
crew = Crew(agents=[news_agent], tasks=[task])
result = crew.kickoff()
```

## 📝 학습 내용

- CrewAI 프레임워크 사용법
- 멀티 에이전트 시스템 설계
- AI Tool 활용 및 통합
- 뉴스 데이터 처리 및 요약
- 에이전트 간 협업 패턴

## 🔐 보안

- `.env` 파일은 `.gitignore`에 포함되어 있어 GitHub에 업로드되지 않습니다.
- API 키는 절대 커밋하지 마세요.

## 📚 참고 자료

- [CrewAI 공식 문서](https://docs.crewai.com/)
- [OpenAI API 문서](https://platform.openai.com/docs)
- [노마드 코더 - AI Agents Masterclass](https://nomadcoders.co/ai-agents-masterclass/lobby)

## 👤 작성자

김정태 ([@Origogi](https://github.com/Origogi))

## 📄 라이선스

이 프로젝트는 학습 목적으로 작성되었습니다.
