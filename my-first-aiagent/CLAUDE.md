# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Python 3.13+ 기반의 OpenAI Function Calling 에이전트 예제 프로젝트입니다.

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
# Python 스크립트 실행
python main.py

# Jupyter 노트북 실행 (VS Code에서)
# main.ipynb 파일 열기
```

### Environment Variables
- `.env` 파일에 환경 변수 저장
- `OPENAI_API_KEY`: OpenAI API 키 필수
- Jupyter 노트북에서는 `python-dotenv`의 `load_dotenv()` 사용 필요

## Project Structure
- `main.py`: 기본 Python 진입점 (Hello World)
- `main.ipynb`: OpenAI Function Calling 구현 Jupyter 노트북
  - Function calling을 사용한 대화형 AI 에이전트
  - Tool 정의 및 매핑 구조
  - 메시지 히스토리 메모라이제이션
- `pyproject.toml`: 프로젝트 메타데이터 및 의존성 (uv 사용)

## Architecture Notes

### Function Calling Pattern (main.ipynb)
- **Tool 정의**: `TOOLS` 리스트에 OpenAI function schema 형식으로 정의
- **Function 매핑**: `FUNCTION_MAPPINGS` 딕셔너리로 함수명-실제 함수 매핑
- **처리 흐름**:
  1. 사용자 입력 → `call_ai()` → OpenAI API 호출
  2. `process_ai_response()` → tool_calls 확인
  3. tool_calls 존재 시 → 함수 실행 → 결과를 메시지에 추가 → 재귀 호출
  4. tool_calls 없으면 → 최종 응답 출력
- **메모라이제이션**: 모든 대화 내역을 `messages` 리스트에 저장

## Dependencies
- **openai**: OpenAI API 클라이언트
- **python-dotenv**: 환경 변수 로드
- **ipykernel**: Jupyter 노트북 지원 (dev)
