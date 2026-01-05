# Finance Advisor Agent

## 프로젝트 개요
Google ADK(Agent Development Kit)와 Firecrawl을 활용한 금융 어드바이저 에이전트 실습 프로젝트입니다.

## 기술 스택
- **Language**: Python 3.13
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Framework**: google-adk
- **Tools**: Firecrawl (Web Search & Scraping)

## 환경 설정
`.env` 파일에 다음 키가 설정되어 있어야 합니다:
- `OPENAI_API_KEY`: LLM 모델 사용을 위한 키
- `FIRECRAWL_API_KEY`: 웹 정보 수집을 위한 키
- `GOOGLE_API_KEY`: (선택 사항) Gemini 모델 사용 시 필요

## 주요 기능
- Firecrawl을 이용한 최신 금융 데이터 수집
- google-adk를 활용한 에이전트 워크플로우 구성
- 실시간 주식 트렌드 및 금융 뉴스 분석

## 실행 방법
```bash
# 의존성 설치
uv sync

# 에이전트 실행
uv run main.py
```
