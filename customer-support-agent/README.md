# Customer Support AI Agent

고객 문의 유형에 따라 적합한 AI Agent로 라우팅하는 시스템 실습 프로젝트

## 개요

이 프로젝트는 고객 지원 시나리오에서 AI Agent를 활용하는 방법을 학습하기 위한 실습용 프로젝트입니다.

### 주요 기능 (예정)
- 고객 문의 분류
- 목적에 맞는 전문 Agent로 라우팅
- 대화 컨텍스트 유지

## 시작하기

### 사전 요구사항
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) 패키지 매니저

### 설치

```bash
# 의존성 설치
uv sync

# 환경변수 설정
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 설정
```

### 실행

```bash
uv run python main.py
```

## 기술 스택

- **Python**: 메인 언어
- **uv**: 패키지 관리
- **OpenAI SDK**: LLM API 연동

## 라이선스

이 프로젝트는 학습 목적으로 제작되었습니다.
