# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python 3.13+ 기반의 News Reader AI Agent 프로젝트입니다. CrewAI 프레임워크를 사용하여 뉴스를 자동으로 수집, 요약, 큐레이션하는 멀티 에이전트 시스템을 구현합니다.

## Development Commands

### Environment Setup
```bash
# 의존성 설치 (uv 패키지 매니저 사용)
uv sync

# 개발 의존성 포함 설치
uv sync --all-groups
```

### Running the Application
```bash
# 메인 애플리케이션 실행
python main.py
```

### Environment Variables
- `.env` 파일에 환경 변수 저장 필수
- `OPENAI_API_KEY`: OpenAI API 키 (필수)

## Architecture Overview

### CrewAI Multi-Agent System
이 프로젝트는 CrewAI의 `@CrewBase` 데코레이터를 사용한 선언적 멀티 에이전트 아키텍처를 따릅니다.

**중요**: `@CrewBase` 데코레이터 사용 시 `Crew` 클래스를 직접 상속하지 않습니다. 데코레이터가 모든 필요한 기능을 자동으로 제공합니다.

### Agent Pipeline (3단계)
1. **News Hunter Agent** (`news_hunter_agent`): 뉴스 검색 및 수집
   - SerperDevTool로 뉴스 검색
   - ScrapeWebsiteTool로 아티클 스크래핑
   - 신뢰도 및 관련성 점수 부여

2. **Summarizer Agent** (`summarizer_agent`): 뉴스 요약
   - 3단계 요약 생성 (헤드라인/요약/상세)
   - OpenAI o3 모델 사용

3. **Curator Agent** (`curator_agent`): 최종 큐레이션 및 리포트 작성
   - 편집 판단 및 우선순위 결정
   - 출판 가능한 최종 리포트 생성

### Configuration Structure
- `config/agents.yaml`: 모든 에이전트의 role, goal, backstory 정의
- `config/tasks.yaml`: 각 에이전트의 작업 description, expected_output, 출력 파일 설정
- `tools.py`: 커스텀 CrewAI 도구 정의 (`@tool` 데코레이터 사용)

### Output Structure
- `output/content_harvest.md`: 1단계 수집된 뉴스 원본
- `output/summary.md`: 2단계 요약 결과
- `output/final_report.md`: 3단계 최종 큐레이션 리포트

## Project Structure

- `main.py`: CrewAI 멀티 에이전트 시스템 진입점
  - `NewsReaderAgent` 클래스가 전체 crew 오케스트레이션 담당
  - `.crew().kickoff()`으로 실행
- `config/`: YAML 기반 에이전트 및 태스크 설정
- `tools.py`: 커스텀 CrewAI 도구
- `output/`: 마크다운 형식의 출력 파일들
- `pyproject.toml`: uv 패키지 매니저 설정
- `.env`: 환경 변수 (git에서 제외됨)

## Key Dependencies

- **crewai[tools]**: 멀티 에이전트 오케스트레이션 프레임워크
- **openai**: OpenAI API 클라이언트
- **python-dotenv**: 환경 변수 로드

## Common Patterns

### Adding New Agents
1. `config/agents.yaml`에 에이전트 정의 추가
2. `main.py`에 `@agent` 데코레이터로 메서드 추가
3. 필요시 `tools.py`에 커스텀 도구 구현

### Adding New Tasks
1. `config/tasks.yaml`에 태스크 정의 추가
2. `main.py`에 `@task` 데코레이터로 메서드 추가
3. `agent` 필드로 담당 에이전트 지정

### Custom Tools
`@tool` 데코레이터 사용하여 함수를 CrewAI 도구로 변환. docstring 필수.
