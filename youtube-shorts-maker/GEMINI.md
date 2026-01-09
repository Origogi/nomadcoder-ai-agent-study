# YouTube Shorts Maker Agent

## 프로젝트 개요
Google ADK(Agent Development Kit)를 활용하여 YouTube Shorts 콘텐츠를 기획하고 제작하는 AI 에이전트 프로젝트입니다.

## 기술 스택
- **Language**: Python 3.13
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Framework**: google-adk
- **Model**: Gemini 2.0 (google-genai)

## 환경 설정
`.env` 파일에 다음 키가 설정되어 있어야 합니다:
- `GOOGLE_API_KEY`: Gemini 모델 사용을 위한 API 키

## 주요 기능
- YouTube Shorts 콘텐츠 기획 (Content Planner Agent)
- Shorts 영상 제작을 위한 스크립트 및 구성안 생성
- google-adk를 활용한 멀티 에이전트 워크플로우

## 실행 방법
```bash
# 의존성 설치
uv sync

# 에이전트 실행
uv run main.py

# ADK 웹 서버 실행 (에이전트 코드 변경 시 자동 리로드)
uv run adk web --reload_agents
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
feat(planner): Shorts 콘텐츠 기획 로직 추가

- 사용자의 주제에 기반한 3가지 다른 스타일의 스크립트 생성 기능 구현
- 시각적 연출을 위한 장면 전환 가이드라인 포함
- content_planner_agent와 메인 에이전트 연결
```

## 서버 실행 최적화 규칙 (Fast Startup)
1. **uv 환경 실행**: 모든 Python 실행 명령(서버, 스크립트 등)은 반드시 `uv run`을 접두어로 사용하여 가상 환경을 로드합니다. (예: `uv run adk web ...`)
2. **버퍼링 해제**: Python 기반 서버 실행 시 `export PYTHONUNBUFFERED=1`을 설정하여 로그가 지연 없이 출력되도록 합니다.
3. **검증 절차 단축**: 백그라운드 실행 후 `ps`로 PID를 확인하는 단계를 생략합니다. 대신 실행 직후 `sleep 1`만 수행하고 즉시 로그 파일(`cat` or `tail`)을 읽습니다.
4. **성공 기준**: 로그 파일에서 'Application startup complete' 문구나 'http://...' URL이 확인되면 즉시 사용자에게 주소를 안내하고 태스크를 완료합니다.

