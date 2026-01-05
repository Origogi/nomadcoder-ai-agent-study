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

## 커밋 메시지 가이드
기본적으로 다음의 템플릿을 준수하며, 한글로 작성합니다.

### 템플릿 형식
```text
<type>(<scope>): <subject>

<body> (선택 사항: 변경 이유와 핵심 변경 내용 설명)
```

### Type 종류
- **feat**: 새로운 기능 추가
- **fix**: 버그 수정
- **docs**: 문서 수정 (README.md, gemini.md 등)
- **style**: 코드 포맷팅, 세미콜론 누락 등 (로직 변경 없음)
- **refactor**: 코드 리팩토링
- **test**: 테스트 코드 추가 및 리팩토링
- **chore**: 패키지 매니저 설정, 빌드 업무 수정 등

### 작성 규칙
1. **Subject**: 50자 이내로 핵심 요약 (끝에 마침표 금지)
2. **Body**: 무엇을, 왜 변경했는지 자세히 설명 (한 줄당 72자 내외 권장)

### 예시
```text
fix(tools): Firecrawl v2 API 호환성 버그 수정

- API 응답 구조가 SearchData 객체로 변경됨에 따라 접근 방식 수정
- 검색 결과에서 markdown 필드가 누락되는 경우에 대한 예외 처리 추가
- 속성 접근 시 getattr을 사용하여 안정성 확보
```

